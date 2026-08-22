from django.db import models
from django.conf import settings


class Habit(models.Model):
    """Модель привычки"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name="Пользователь"
    )
    place = models.CharField(
        max_length=255,
        verbose_name="Место выполнения"
    )
    time = models.TimeField(
        verbose_name="Время выполнения"
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие"
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки"
    )
    linked_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        help_text="Может быть указана только для полезных привычек"
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Периодичность (дни)",
        help_text="Не реже 1 раза в 7 дней"
    )
    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Вознаграждение"
    )
    time_to_complete = models.PositiveSmallIntegerField(
        verbose_name="Время на выполнение (сек)",
        help_text="Не более 120 секунд"
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна"
    )

    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ['-id']
