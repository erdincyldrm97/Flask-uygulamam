from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
import asyncio
import requests
import talib
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# Telegram Bot Token ve CoinMarketCap API Anahtarı
TOKEN = "7867509256:AAF0Vk44_F0_Otxbfkr87LUVMmh2f6hy7kA"
API_KEY = "00f75cc8-e140-4e37-acc0-fa98a7f8279e"

bot = Bot(token=TOKEN)
dp = Dispatcher()

def format_price(price):
    """Fiyatı uygun ondalık hassasiyetine göre biçimlendirir."""
    if price >= 1:
        return f"{price:.2f}"
    elif price >= 0.001:
        return f"{price:.4f}"
    else:
        return f"{price:.6f}"

def get_price(coin: str):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": API_KEY}
    params = {"symbol": coin, "convert": "USD"}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if "data" in data and coin in data["data"]:
        coin_data = data["data"][coin]
        price = coin_data["quote"]["USD"]["price"]
        return {
            "price": price,
            "formatted_price": format_price(price),
            "percent_change_24h": coin_data["quote"]["USD"]["percent_change_24h"]
        }
    return None

def get_historical_data(coin: str, days: int = 90):
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {"fsym": coin, "tsym": "USD", "limit": days}
    response = requests.get(url, params=params)
    data = response.json()
    if "Data" in data and "Data" in data["Data"]:
        historical_data = data["Data"]["Data"]
        close_prices = [day["close"] for day in historical_data]
        return close_prices
    return None

def calculate_technical_indicators(prices):
    prices = np.array(prices)
    rsi = talib.RSI(prices, timeperiod=14)[-1]
    macd, macdsignal, _ = talib.MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9)
    sma_50 = talib.SMA(prices, timeperiod=50)[-1]
    sma_200 = talib.SMA(prices, timeperiod=200)[-1]
    upper_band, _, lower_band = talib.BBANDS(prices, timeperiod=20, nbdevup=2, nbdevdn=2)
    stoch_rsi = talib.STOCHRSI(prices, timeperiod=14, fastk_period=3, fastd_period=3)[-1]
    return {
        "rsi": rsi,
        "macd": macd[-1],
        "macdsignal": macdsignal[-1],
        "sma_50": sma_50,
        "sma_200": sma_200,
        "upper_band": upper_band[-1],
        "lower_band": lower_band[-1],
        "stoch_rsi_k": stoch_rsi[0],
        "stoch_rsi_d": stoch_rsi[1]
    }

def calculate_support_resistance(prices):
    return min(prices[-10:]), max(prices[-10:])

def trade_signal(price, indicators, support, resistance):
    rsi = indicators["rsi"]
    macd = indicators["macd"]
    macdsignal = indicators["macdsignal"]
    sma_50 = indicators["sma_50"]
    sma_200 = indicators["sma_200"]
    upper_band = indicators["upper_band"]
    lower_band = indicators["lower_band"]
    stoch_rsi_k = indicators["stoch_rsi_k"]
    stoch_rsi_d = indicators["stoch_rsi_d"]

    signal = ""

    # **Kısa Vadeli Alım/Satım Önerisi**
    buy_zone = support * 1.02  # Destek seviyesinin biraz üstü
    sell_zone = resistance * 0.98  # Direnç seviyesinin biraz altı

    signal += f"✅ **Kısa Vadeli Alım Bölgesi**: **${format_price(buy_zone)} - ${format_price(support)}** _(Destek yakınında)_\n"
    signal += f"❌ **Kısa Vadeli Satış Bölgesi**: **${format_price(sell_zone)} - ${format_price(resistance)}** _(Direnç yakınında)_\n"

    # **Uzun Vadeli Trend Analizi**
    if sma_50 > sma_200:
        signal += "✅ **Uzun Vadeli Alım Önerisi**: SMA50, SMA200'ü yukarı kesmiş.\n"
    else:
        signal += "⚠️ **Uzun Vadeli Satış Önerisi**: SMA50, SMA200'ün altında.\n"

    # **Bollinger Bantları Analizi**
    if price > upper_band:
        signal += "🚨 **Bollinger Üst Bandı**: Aşırı alım (Dikkatli olun).\n"
    elif price < lower_band:
        signal += "💰 **Bollinger Alt Bandı**: Aşırı satım (Fırsat olabilir).\n"

    # **Stochastic RSI Analizi**
    if stoch_rsi_k > 80 and stoch_rsi_d > 80:
        signal += "🚨 **Stochastic RSI**: Aşırı alım (Dikkatli olun).\n"
    elif stoch_rsi_k < 20 and stoch_rsi_d < 20:
        signal += "💰 **Stochastic RSI**: Aşırı satım (Fırsat olabilir).\n"

    # **Destek ve Direnç Seviyeleri**
    signal += f"\n📉 **Destek Seviyesi**: ${format_price(support)}\n"
    signal += f"📈 **Direnç Seviyesi**: ${format_price(resistance)}\n"

    return signal

def plot_price_chart(prices, coin):
    plt.figure(figsize=(10, 5))
    plt.plot(prices, label=f"{coin} Fiyat")
    plt.title(f"{coin} Fiyat Grafiği")
    plt.xlabel("Gün")
    plt.ylabel("Fiyat (USD)")
    plt.legend()
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf

@dp.message(Command(commands=["price"]))
async def price_command(message: Message):
    try:
        coin = message.text.split()[1].upper()
        coin_data = get_price(coin)
        if coin_data:
            price = coin_data["price"]
            formatted_price = coin_data["formatted_price"]
            percent_change_24h = coin_data["percent_change_24h"]

            historical_data = get_historical_data(coin)
            if historical_data:
                indicators = calculate_technical_indicators(historical_data)
                support, resistance = calculate_support_resistance(historical_data)

                analysis = f"✅ **{coin} Alım/Satım Analizi**:\n\n"
                analysis += f"💰 **Fiyat**: ${formatted_price}\n"
                analysis += f"📊 **24h Yüzde Değişim**: %{round(percent_change_24h, 2)}\n"
                analysis += f"📈 **RSI**: {round(indicators['rsi'], 2)}\n"
                analysis += f"📉 **MACD**: {round(indicators['macd'], 2)}\n"
                analysis += f"📊 **MACD Signal**: {round(indicators['macdsignal'], 2)}\n"
                analysis += f"📈 **SMA 50**: {format_price(indicators['sma_50'])}\n"
                analysis += f"📉 **SMA 200**: {format_price(indicators['sma_200'])}\n"
                analysis += f"📊 **Bollinger Üst Band**: {format_price(indicators['upper_band'])}\n"
                analysis += f"📉 **Bollinger Alt Band**: {format_price(indicators['lower_band'])}\n"
                analysis += f"📊 **Stochastic RSI K**: {round(indicators['stoch_rsi_k'], 2)}\n"
                analysis += f"📉 **Stochastic RSI D**: {round(indicators['stoch_rsi_d'], 2)}\n"

                # Ticaret sinyali ekleme
                signal = trade_signal(price, indicators, support, resistance)
                analysis += f"\n🚀 **Ticaret Sinyali**:\n{signal}\n"

                # Fiyat grafiği oluşturma
                chart = plot_price_chart(historical_data, coin)
                await message.answer_photo(photo=chart, caption=analysis)
            else:
                await message.answer(f"{coin} için geçmiş veri bulunamadı.")
        else:
            await message.answer(f"{coin} hakkında veri bulunamadı veya API hatası oluştu.")
    except IndexError:
        await message.answer("Lütfen bir coin adı gir. Örn: /price BTC")
    except TelegramBadRequest as e:
        await message.answer(f"Telegram hatası: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())