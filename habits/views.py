# from django.db import models
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnly
from .pagination import HabitPagination


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для привычек"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = HabitPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_public', 'is_pleasant', 'is_active']
    ordering_fields = ['time', 'periodicity']

    # def get_queryset(self):
    #     """Возвращаем привычки пользователя ИЛИ публичные."""
    #     user = self.request.user
    #     return Habit.objects.filter(
    #         models.Q(user=user) | models.Q(is_public=True, is_active=True)
    #     ).distinct()

    def get_queryset(self):
        """Возвращаем только свои привычки."""
        user = self.request.user
        return Habit.objects.filter(user=user, is_active=True)

    def perform_create(self, serializer):
        """При создании проставляем пользователя."""
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        """Передаём request в сериализатор."""
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def public(self, request):
        """Эндпоинт для списка публичных привычек (доступен без авторизации)."""
        habits = Habit.objects.filter(is_public=True, is_active=True)
        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)
