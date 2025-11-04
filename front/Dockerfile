# Базовый образ
FROM node:20-alpine

# Создаем директорию приложения
WORKDIR /front

# Устанавливаем зависимости
COPY package.json .

# Установим зависимости
RUN npm install

# Команда запуска
CMD ["tail", "-f", "/dev/null"]