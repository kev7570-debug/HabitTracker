from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'place', 'time', 'is_pleasant', 'is_public', 'is_active', 'periodicity')
    list_filter = ('is_pleasant', 'is_public', 'periodicity')
    search_fields = ('action', 'place', 'user__email')
    # readonly_fields = ('user',)
    fieldsets = (
        ('Основное', {
            'fields': ('user', 'action', 'place', 'time')
        }),
        ('Дополнительно', {
            'fields': ('is_pleasant', 'linked_habit', 'reward', 'periodicity', 'time_to_complete', 'is_public', 'is_active')
        }),
    )
