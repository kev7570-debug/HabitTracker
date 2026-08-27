from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .models import TelegramUser

User = get_user_model()


class TelegramUserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )

    def test_create_telegram_user(self):
        tg_user = TelegramUser.objects.create(
            user=self.user,
            chat_id='123456789'
        )
        self.assertEqual(tg_user.user.email, 'test@example.com')
        self.assertEqual(tg_user.chat_id, '123456789')
        self.assertIsNotNone(tg_user.created_at)


class TelegramConnectAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='api@example.com',
            first_name='Api',
            last_name='User',
            password='apipass123'
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_connect_telegram_success(self):
        url = '/api/telegram/connect/'
        data = {'chat_id': '987654321'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chat_id'], '987654321')
        self.assertTrue(TelegramUser.objects.filter(chat_id='987654321').exists())

    def test_connect_telegram_missing_chat_id(self):
        url = '/api/telegram/connect/'
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('chat_id обязателен', str(response.data))

    def test_connect_telegram_without_auth(self):
        self.client.credentials()  # удаляем токен
        url = '/api/telegram/connect/'
        data = {'chat_id': '111111111'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
