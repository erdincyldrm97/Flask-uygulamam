# Python 3.10 imajını kullan
FROM python:3.10-slim

# Gerekli sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    gfortran \
    wget \
    && rm -rf /var/lib/apt/lists/*

# TA-Lib'i kaynak kodundan indir ve kur
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Çalışma dizinini belirle
WORKDIR /app

# requirements.txt dosyasını kopyala
COPY requirements.txt .

# pip güncelle
RUN pip install --upgrade pip

# Gereksinimleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulamayı başlat
COPY . /app
CMD ["python", "main.py"]