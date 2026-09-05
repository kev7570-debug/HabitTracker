from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit"""

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, data):
        """
        Валидация привычки.
        Проверяем все 5 правил из ТЗ.
        """
        is_pleasant = data.get('is_pleasant', False)
        linked_habit = data.get('linked_habit')
        reward = data.get('reward')
        time_to_complete = data.get('time_to_complete')
        periodicity = data.get('periodicity', 1)

        # 1. Нельзя одновременно заполнять reward и linked_habit
        if reward and linked_habit:
            raise serializers.ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )

        # 2. Время выполнения не должно превышать 120 секунд
        if time_to_complete and time_to_complete > 120:
            raise serializers.ValidationError(
                "Время на выполнение не должно превышать 120 секунд."
            )

        # 3. В linked_habit можно передать только привычку с is_pleasant=True
        if linked_habit:
            if not linked_habit.is_pleasant:
                raise serializers.ValidationError(
                    "Связанная привычка должна быть приятной (is_pleasant=True)."
                )

        # 4. У приятной привычки не может быть reward или linked_habit
        if is_pleasant:
            if reward:
                raise serializers.ValidationError(
                    "У приятной привычки не может быть вознаграждения."
                )
            if linked_habit:
                raise serializers.ValidationError(
                    "У приятной привычки не может быть связанной привычки."
                )

        # 5. Периодичность от 1 до 7 дней
        if periodicity < 1 or periodicity > 7:
            raise serializers.ValidationError(
                "Периодичность должна быть от 1 до 7 дней (не реже раза в неделю)."
            )

        return data

    def create(self, validated_data):
        """При создании автоматически проставляем пользователя"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)
