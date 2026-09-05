from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import TelegramUser


class TelegramConnectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        chat_id = request.data.get('chat_id')
        if not chat_id:
            return Response(
                {'error': 'chat_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        telegram_user, created = TelegramUser.objects.get_or_create(
            user=request.user,
            defaults={'chat_id': chat_id}
        )
        if not created:
            telegram_user.chat_id = chat_id
            telegram_user.save()

        return Response(
            {'message': 'Telegram привязан', 'chat_id': chat_id},
            status=status.HTTP_200_OK
        )
