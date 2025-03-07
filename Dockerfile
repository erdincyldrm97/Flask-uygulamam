# Python 3.10 veya 3.11 tabanlı bir imaj kullan
FROM python:3.10

# Çalışma dizinini belirle
WORKDIR /app

# Gerekli dosyaları kopyala
COPY . /app/

# Pip'in güncellendiğinden emin ol ve bağımlılıkları yükle
RUN pip install --upgrade pip && pip install -r requirements.txt

# Ana dosyayı çalıştır
CMD ["python", "main.py"]