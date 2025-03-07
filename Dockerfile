# Python 3.10 veya 3.11 kullan
FROM python:3.10

# Gerekli bağımlılıkları yükle (TA-Lib için gerekli)
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libta-lib-dev \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizinini belirle
WORKDIR /app

# Gerekli dosyaları kopyala
COPY . /app/

# Pip'in güncellendiğinden emin ol ve bağımlılıkları yükle
RUN pip install --upgrade pip && pip install -r requirements.txt

# Ana dosyayı çalıştır
CMD ["python", "main.py"]