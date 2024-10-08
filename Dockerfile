# Базовый образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 80
EXPOSE 80

# Команда для запуска приложения с использованием waitress
CMD ["python", "-m", "waitress", "--host=0.0.0.0", "--port=80", "main:app"]
