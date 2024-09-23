
# Diary Project

## Описание проекта
Diary Project — это веб-приложение для ведения личного дневника. Пользователи могут создавать, редактировать и удалять записи, добавлять свои записи в воспоминания, которые будут отправлены в Telegram, в установленное пользователем время. Приложение поддерживает аутентификацию, CRUD операции для записей дневника и напоминаний, а также использование Celery для задач по расписанию. Реализована автоматическая модерация нактивных пользователей и возможность модерирования обьектов моделей, а так же ик создателей, с помощью кастомных прав.

## Используемые технологии
- Django
- Celery
- PostgreSQL
- Docker
- Redis


## Установка и запуск проекта

### 1. Клонирование репозитория
```bash
git clone https://github.com/SilverAnton/Diary_proj.git
cd diary_project
```

### 2. Установка зависимостей и создание базы данных
Создайте виртуальное окружение и установите зависимости:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Создание базы данных

После клонирования репозитория и установки зависимостей, необходимо создать базу данных PostgreSQL.

 Подключитесь к PostgreSQL:
   ```bash
   psql -U postgres
   ```
Создайте новую базу данных:
   ```
   CREATE DATABASE your_database_name;
   ```

### 3. Настройка окружения
Создайте файл `.env` на основе примера `.env.example` и заполните его необходимыми значениями:
```dotenv
SECRET_KEY=your_secret_key
DEBUG=True
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
EMAIL_HOST=your_email_host
EMAIL_PORT=your_email_port
EMAIL_HOST_USER=your_email_user
EMAIL_HOST_PASSWORD=your_email_password
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

### 4. Запуск проекта с использованием Docker
Соберите и запустите контейнеры:
```bash
docker-compose up --build
```

Создайте суперпользователя:
```bash
docker-compose exec app python manage.py createsuperuser
```

Создайте нового пользователя используя команду из приложения users:
```bash
docker exec -it diary_proj-app-1 python manage.py cu
```

## Структура проекта

- **users**: Приложение для управления пользователями. Кастомная модель пользователя, аутентификация, регистрация.
- **diary**: Приложение для работы с записями дневника. CRUD операции, поиск по записям.
- **memories**: Приложение для создания и управления воспоминаниями. Воспоминания отправляются в Telegram с использованием Celery.
- **static**: Статические файлы (CSS).
- **templates**: Шаблоны HTML.

## Дополнительная информация
- **Настройки Celery**: Celery используется для выполнения фоновых задач и задач по расписанию.
- **Настройки почты**: Django настроен для отправки писем через SMTP.
```
