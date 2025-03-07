# Python 3.10 tabanlı imajı kullan
FROM python:3.10

# Gerekli bağımlılıkları yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# TA-Lib kaynak kodlarını indir, doğrula ve derle
RUN wget -O ta-lib-0.4.0-src.tar.gz "http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz" && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    ls -la && \
    mv ta-lib ta-lib-0.4.0 && \
    cd ta-lib-0.4.0 && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib-0.4.0 ta-lib-0.4.0-src.tar.gz

# Çalışma dizinini belirle
WORKDIR /app

# Proje dosyalarını kopyala
COPY . /app/

# Pip güncelle ve bağımlılıkları yükle
RUN pip install --upgrade pip && pip install -r requirements.txt

# Uygulamayı başlat
CMD ["python", "main.py"]