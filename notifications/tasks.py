from celery import shared_task
import requests
from django.conf import settings
from habits.models import Habit


@shared_task
def send_habit_notification(habit_id):
    """Отправка уведомления о привычке в Telegram."""
    try:
        habit = Habit.objects.get(id=habit_id, is_active=True)
    except Habit.DoesNotExist:
        print(f"Привычка с ID {habit_id} не найдена или неактивна")
        return

    # Пока используем заглушку для chat_id
    # Позже добавим модель TelegramUser
    chat_id = settings.TELEGRAM_CHAT_ID  # временно

    if not chat_id:
        print("Chat ID не указан")
        return

    message = (
        f"🔔 Напоминание о привычке!\n\n"
        f"Действие: {habit.action}\n"
        f"Место: {habit.place}\n"
        f"Время: {habit.time}\n"
        f"Выполнить за {habit.time_to_complete} сек."
    )

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Уведомление отправлено для привычки {habit_id}")
    except Exception as e:
        print(f"Ошибка при отправке: {e}")
        