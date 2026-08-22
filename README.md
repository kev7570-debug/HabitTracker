# Трекер полезных привычек (Habit Tracker)

API для управления полезными привычками с авторизацией, напоминаниями через Telegram и документацией Swagger.

## 🚀 Стек технологий

- **Python 3.13**
- **Django 4.2.7**
- **Django REST Framework 3.14.0**
- **PostgreSQL** (или SQLite для разработки)
- **JWT-авторизация** (SimpleJWT)
- **Celery + Redis** (фоновые задачи)
- **Telegram Bot API** (уведомления)
- **drf-yasg** (Swagger/ReDoc документация)
- **pytest + coverage** (тестирование)

---

## 📦 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/kev7570-debug/HabitTracker.git
cd HabitTracker
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

#### 📄 Документация API
После запуска сервера документация доступна по адресам:
Swagger UI: http://localhost:8000/swagger/
ReDoc: http://localhost:8000/redoc/

🔔 Настройка Celery (фоновые задачи)

Запуск Redis
Убедитесь, что Redis запущен:

```bash
redis-server
```

Запуск Celery Worker

```bash
celery -A config worker -l INFO --pool=solo
```

Запуск Celery Beat (планировщик)

```bash
celery -A config beat -l INFO
```

##### 📦 Структура проекта
Kursovaya_5/
├── config/                # Настройки проекта
├── users/                 # Пользователи и JWT
├── habits/                # Основная логика (привычки)
├── notifications/         # Уведомления (Telegram + Celery)
├── requirements.txt       # Зависимости
├── .env.template          # Шаблон переменных окружения
└── README.md              # Этот файл


###### ✨ Основные эндпоинты
Метод	URL	                Описание
POST	/api/token/	        Получение JWT-токена
POST	/api/register/	    Регистрация пользователя
GET	    /api/habits/	    Список привычек (пагинация 5)
POST	/api/habits/	    Создание привычки
GET	    /api/habits/{id}/	Просмотр привычки
PATCH	/api/habits/{id}/	Обновление привычки
DELETE	/api/habits/{id}/	Удаление привычки (мягкое)
GET	    /api/habits/public/	Публичные привычки

###### 👤 Права доступа
Каждый пользователь видит и редактирует только свои привычки.
Публичные привычки доступны всем на чтение.
Для создания/редактирования требуется JWT-токен.

###### 🛠 Валидаторы
Нельзя одновременно указать reward и linked_habit
time_to_complete ≤ 120 секунд
linked_habit может быть только приятной привычкой
У приятной привычки нет reward и linked_habit
Периодичность от 1 до 7 дней

🧑‍💻 Автор
[Elena Kashina] — курсовая работа в рамках обучения Django REST Framework.
