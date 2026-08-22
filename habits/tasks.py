from celery import shared_task
from .models import Habit
from notifications.tasks import send_habit_notification


@shared_task
def check_habits():
    """Проверка привычек и отправка уведомлений."""
    from datetime import datetime
    now = datetime.now().time()

    habits = Habit.objects.filter(
        is_active=True,
        time__lte=now
    )

    for habit in habits:
        send_habit_notification.delay(habit.id)
