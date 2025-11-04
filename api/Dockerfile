# Базовый образ (лучше брать slim, чтобы не был слишком тяжёлый)
FROM python:3.11-slim

# Установим рабочую директорию внутри контейнера
WORKDIR /api

# Скопируем файл с зависимостями, если он есть (например requirements.txt)
COPY requirements.txt .

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

CMD ["tail", "-f", "/dev/null"]