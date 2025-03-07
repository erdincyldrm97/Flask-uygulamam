# Temel Python 3.10 slim imajını kullanıyoru
FROM python:3.10-slim

# Çalışma dizini oluşturuyoruz
WORKDIR /app

# Sistem bağımlılıklarını yüklemek için apt-get kullanıyoruz
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libtool \
    pkg-config \
    libta-lib-dev && \
    rm -rf /var/lib/apt/lists/*

# Gereksinimler dosyasını konteynıra kopyalıyoruz
COPY requirements.txt .

# Python bağımlılıklarını yüklüyoruz
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını konteynıra kopyalıyoruz
COPY . .

# Uygulama için gerekli portu açıyoruz
EXPOSE 8000

# Uygulama başlatma komutunu belirtiyoruz
CMD ["python", "main.py"]