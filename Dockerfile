# Python 3.10 slim image'ını kullanıyoruz
FROM python:3.10-slim

# Sistem paketlerini güncelle ve gerekli araçları kur
RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    gfortran \
    wget \
    libffi-dev \
    git \
    autoconf \
    libtool \
    automake \
    && rm -rf /var/lib/apt/lists/*

# TA-Lib'i GitHub'dan klonla ve kur
RUN git clone https://github.com/mrjbq7/ta-lib.git && \
    cd ta-lib && \
    autoreconf --install && \  # Autoreconf ile configure dosyasını oluştur
    RUN ./configure --prefix=/usr && \  # RUN komutu eklenmeli
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib

# Çalışma dizinine geç
WORKDIR /app

# requirements.txt dosyasını kopyala
COPY requirements.txt .

# pip'i güncelle
RUN pip install --upgrade pip

# Gerekli Python paketlerini yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodlarını kopyala
COPY . /app

# Uygulamanı başlat
CMD ["python", "main.py"]