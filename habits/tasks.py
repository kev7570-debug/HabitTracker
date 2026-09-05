from celery import shared_task
from .models import Habit
from notifications.tasks import send_habit_notification
from datetime import datetime, timezone


# @shared_task
# def check_habits():
#     """Проверка привычек и отправка уведомлений."""
#     from datetime import datetime
#     now = datetime.now().time()
#
#     habits = Habit.objects.filter(
#         is_active=True,
#         time__lte=now
#     )
#
#     for habit in habits:
#         send_habit_notification.delay(habit.id)

@shared_task
def check_habits():
    """Проверка привычек и отправка уведомлений (без спама)."""
    now = datetime.now(timezone.utc).time()
    today = datetime.now(timezone.utc).date()

    habits = Habit.objects.filter(
        is_active=True,
        time__lte=now
    )

    for habit in habits:
        # Если уведомление уже отправлялось сегодня — пропускаем
        if habit.last_notified and habit.last_notified.date() == today:
            continue

        send_habit_notification.delay(habit.id)
