# Базовый образ Python
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт
EXPOSE 8000

# Запуск миграций, сборка статики и запуск сервера
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn sales_trading.wsgi:application --bind 0.0.0.0:8000"]
