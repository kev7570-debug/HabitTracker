# Трекер полезных привычек (Habit Tracker)

API для управления полезными привычками с авторизацией, напоминаниями через Telegram и документацией Swagger.

---

## 🚀 Стек технологий

- **Python 3.13**
- **Django 4.2.7**
- **Django REST Framework 3.14.0**
- **PostgreSQL** (продакшен) / SQLite (тесты)
- **JWT-авторизация** (SimpleJWT)
- **Celery + Redis** (фоновые задачи)
- **Telegram Bot API** (уведомления)
- **drf-yasg** (Swagger/ReDoc документация)
- **Docker + Docker Compose** (контейнеризация)
- **GitHub Actions** (CI/CD)

---

## 📦 Локальный запуск через Docker

### 1. Клонирование репозитория
```bash
git clone https://github.com/kev7570-debug/HabitTracker.git
cd HabitTracker
```

### 2. Создание файла .env
Скопируй .env.template в .env и заполни своими значениями:
```bash
cp .env.template .env
```
Важно: для работы в Docker установи DB_HOST=db.

### 3. Запуск проекта
```bash
docker-compose up -d
```

### 4. Применение миграций
```bash
docker-compose exec web python manage.py migrate
```

### 5. Создание суперпользователя
```bash
docker-compose exec web python manage.py createsuperuser
```

### 6. Проверка
Открой в браузере: http://localhost:8000

## 🚀 Деплой на сервер (Yandex Cloud)

### 1. Настройка виртуальной машины
* Создай ВМ с Ubuntu 24.04.
* Добавь SSH-ключ (публичный).
* Установи Docker и Docker Compose:
```bash
sudo apt update && sudo apt install docker.io docker-compose -y
sudo usermod -aG docker $USER
```

### 2. Секреты в GitHub
Добавь в репозиторий → Settings → Secrets and variables → Actions:

Секрет	            Значение
SSH_KEY	            Приватный SSH-ключ (cat ~/.ssh/id_rsa)
SSH_USER	        user (логин на сервере)
SERVER_IP	        Публичный IP ВМ
DEPLOY_DIR	        /home/user/habit-tracker/HabitTracker
SECRET_KEY	        Ключ Django из .env
DB_NAME	            tracker_habits
DB_USER	            postgres
DB_PASSWORD	        Пароль от БД
TELEGRAM_BOT_TOKEN	Токен бота
TELEGRAM_CHAT_ID	Ваш chat_id

### 3. Автоматический деплой
1. Создайте Pull Request из `feature/task_03` → `develop`.
2. После проверки и одобрения выполните слияние в `develop`, затем в `main`.
3. GitHub Actions автоматически запустит деплой на сервер.

### 4. Проверка
Сайт будет доступен по IP сервера:
http://<IP_сервера>:8000

## 🔔 Настройка Celery (фоновые задачи)
### Запуск Redis
Убедитесь, что Redis запущен:
```bash
redis-server
```

### Запуск Celery Worker
```bash
celery -A config worker -l INFO --pool=solo
```

### Запуск Celery Beat (планировщик)
```bash
celery -A config beat -l INFO
```

## 📄 Документация API
После запуска сервера документация доступна по адресам:
Swagger UI: http://localhost:8000/swagger/
ReDoc: http://localhost:8000/redoc/

## 📁 Структура проекта
Kursovaya_5/
├── config/                # Настройки проекта
├── users/                 # Пользователи и JWT
├── habits/                # Основная логика (привычки)
├── notifications/         # Уведомления (Telegram + Celery)
├── .github/workflows/     # CI/CD пайплайны
├── Dockerfile             # Docker-образ приложения
├── docker-compose.yml     # Запуск всех сервисов
├── nginx.conf             # Конфигурация Nginx
├── requirements.txt       # Зависимости
├── .env.template          # Шаблон переменных окружения
└── README.md              # Этот файл

## ✨ Основные эндпоинты
Метод	URL	                Описание
POST	/api/token/	        Получение JWT-токена
POST	/api/register/	    Регистрация пользователя
GET	    /api/habits/	    Список привычек 
POST	/api/habits/	    Создание привычки
GET	    /api/habits/{id}/	Просмотр привычки
PATCH	/api/habits/{id}/	Обновление привычки
DELETE	/api/habits/{id}/	Удаление привычки 
GET	    /api/habits/public/	Публичные привычки

## 👤 Права доступа
* Каждый пользователь видит и редактирует только свои привычки.
* Публичные привычки доступны всем на чтение.
* Для создания/редактирования требуется JWT-токен.

## 🛠 Валидаторы
* Нельзя одновременно указать reward и linked_habit.
* time_to_complete ≤ 120 секунд.
* linked_habit может быть только приятной привычкой.
* У приятной привычки нет reward и linked_habit.
* Периодичность от 1 до 7 дней.

## 🧑‍💻 Автор
[Elena Kashina] — курсовая работа в рамках обучения Django REST Framework.
