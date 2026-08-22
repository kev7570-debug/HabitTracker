from django.test import TestCase
from django.contrib.auth import get_user_model
from habits.models import Habit
from habits.serializers import HabitSerializer
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class HabitModelTest(TestCase):
    """Тесты для модели Habit"""

    def setUp(self):
        """Создаём тестового пользователя и привычку"""
        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place='Дома',
            time='12:00:00',
            action='Пить воду',
            is_pleasant=False,
            periodicity=1,
            time_to_complete=60,
            is_public=False,
            is_active=True
        )

    def test_habit_creation(self):
        """Тест: привычка создаётся корректно"""
        self.assertEqual(self.habit.user.email, 'test@example.com')
        self.assertEqual(self.habit.action, 'Пить воду')
        self.assertEqual(self.habit.place, 'Дома')
        self.assertEqual(self.habit.time_to_complete, 60)
        self.assertTrue(self.habit.is_active)

    def test_habit_str(self):
        """Тест: строковое представление привычки"""
        expected = f"{self.habit.action} в {self.habit.time} в {self.habit.place}"
        self.assertEqual(str(self.habit), expected)

    def test_habit_is_pleasant_default_false(self):
        """Тест: по умолчанию привычка не приятная"""
        self.assertFalse(self.habit.is_pleasant)

    def test_habit_is_public_default_false(self):
        """Тест: по умолчанию привычка не публичная"""
        self.assertFalse(self.habit.is_public)

    def test_habit_is_active_default_true(self):
        """Тест: по умолчанию привычка активна"""
        self.assertTrue(self.habit.is_active)

    def test_periodicity_default_one(self):
        """Тест: периодичность по умолчанию = 1 день"""
        self.assertEqual(self.habit.periodicity, 1)

class HabitSerializerTest(TestCase):
    """Тесты для сериализатора HabitSerializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )

    def test_valid_data(self):
        """Тест: сериализатор принимает корректные данные"""
        data = {
            'place': 'Работа',
            'time': '09:00:00',
            'action': 'Сделать зарядку',
            'is_pleasant': False,
            'periodicity': 1,
            'time_to_complete': 60,
            'is_public': False,
            'is_active': True
        }
        serializer = HabitSerializer(data=data, context={'request': None})
        self.assertTrue(serializer.is_valid())

    def test_time_to_complete_too_long(self):
        """Тест: время выполнения не может превышать 120 секунд"""
        data = {
            'place': 'Работа',
            'time': '09:00:00',
            'action': 'Сделать зарядку',
            'is_pleasant': False,
            'periodicity': 1,
            'time_to_complete': 150,
            'is_public': False,
            'is_active': True
        }
        serializer = HabitSerializer(data=data, context={'request': None})
        self.assertFalse(serializer.is_valid())
        self.assertIn('Время на выполнение не должно превышать 120 секунд', str(serializer.errors))

    def test_reward_and_linked_habit_together(self):
        """Тест: нельзя одновременно указать reward и linked_habit"""
        habit = Habit.objects.create(
            user=self.user,
            place='Дома',
            time='12:00:00',
            action='Приятная привычка',
            is_pleasant=True,
            periodicity=1,
            time_to_complete=30,
            is_public=False,
            is_active=True
        )
        data = {
            'place': 'Работа',
            'time': '09:00:00',
            'action': 'Полезная привычка',
            'is_pleasant': False,
            'periodicity': 1,
            'time_to_complete': 60,
            'reward': 'Шоколадка',
            'linked_habit': habit.id,
            'is_public': False,
            'is_active': True
        }
        serializer = HabitSerializer(data=data, context={'request': None})
        self.assertFalse(serializer.is_valid())


class HabitAPITest(APITestCase):
    """Тесты для API эндпоинтов привычек"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            first_name='Other',
            last_name='User',
            password='otherpass123'
        )
        # Получаем токен для пользователя
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.habit = Habit.objects.create(
            user=self.user,
            place='Дома',
            time='12:00:00',
            action='Пить воду',
            is_pleasant=False,
            periodicity=1,
            time_to_complete=60,
            is_public=False,
            is_active=True
        )

    def test_get_habits_list(self):
        """Тест: получение списка привычек"""
        url = '/api/habits/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_habit(self):
        """Тест: создание привычки"""
        url = '/api/habits/'
        data = {
            'place': 'Работа',
            'time': '09:00:00',
            'action': 'Сделать зарядку',
            'is_pleasant': False,
            'periodicity': 1,
            'time_to_complete': 60,
            'is_public': False,
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['action'], 'Сделать зарядку')

    def test_get_public_habits(self):
        """Тест: получение публичных привычек (без авторизации)"""
        # Создаём публичную привычку
        public_habit = Habit.objects.create(
            user=self.user,
            place='Парк',
            time='10:00:00',
            action='Гулять',
            is_pleasant=False,
            periodicity=1,
            time_to_complete=30,
            is_public=True,
            is_active=True
        )
        # Сбрасываем авторизацию
        self.client.credentials()
        url = '/api/habits/public/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['action'], 'Гулять')

    def test_update_own_habit(self):
        """Тест: обновление своей привычки"""
        url = f'/api/habits/{self.habit.id}/'
        data = {'place': 'Новое место'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 'Новое место')

    def test_cannot_update_others_habit(self):
        """Тест: нельзя обновить чужую привычку"""
        other_habit = Habit.objects.create(
            user=self.other_user,
            place='Чужое место',
            time='08:00:00',
            action='Чужое действие',
            is_pleasant=False,
            periodicity=1,
            time_to_complete=30,
            is_public=False,
            is_active=True
        )
        url = f'/api/habits/{other_habit.id}/'
        data = {'place': 'Попытка изменить'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
