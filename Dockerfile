# Python 3.10 imajını kullan
FROM python:3.10-slim

# Gerekli sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    gfortran \
    libta-lib0-dev \
    && rm -rf /var/lib/apt/lists/*

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