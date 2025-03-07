# Python 3.10 veya 3.11 kullan
FROM python:3.10

# Gerekli bağımlılıkları yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# TA-Lib kaynak kodlarını indir ve derle
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib-0.4.0 && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib-0.4.0 ta-lib-0.4.0-src.tar.gz

# Çalışma dizinini belirle
WORKDIR /app

# Gerekli dosyaları kopyala
COPY . /app/

# Pip'in güncellendiğinden emin ol ve bağımlılıkları yükle
RUN pip install --upgrade pip && pip install -r requirements.txt

# Ana dosyayı çalıştır
CMD ["python", "main.py"]