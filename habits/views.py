# from django.db import models
# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import OrderingFilter
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
#
# from .models import Habit
# from .serializers import HabitSerializer
# from .permissions import IsOwnerOrReadOnly
# from .pagination import HabitPagination
#
# @csrf_exempt
# def public_habits_list(request):
#     habits = Habit.objects.filter(is_public=True, is_active=True)
#     data = [
#         {
#             'id': h.id,
#             'action': h.action,
#             'place': h.place,
#             'time': h.time,
#             'is_pleasant': h.is_pleasant,
#             'periodicity': h.periodicity,
#         }
#         for h in habits
#     ]
#     return JsonResponse(data, safe=False)
#
# class HabitViewSet(viewsets.ModelViewSet):
#     """ViewSet для привычек"""
#     serializer_class = HabitSerializer
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
#     pagination_class = HabitPagination
#     filter_backends = [DjangoFilterBackend, OrderingFilter]
#     filterset_fields = ['is_public', 'is_pleasant', 'is_active']
#     ordering_fields = ['time', 'periodicity', 'created_at']
#
#     def get_queryset(self):
#         """
#         Возвращаем привычки пользователя ИЛИ публичные.
#         """
#         user = self.request.user
#         # Свои привычки + публичные (на чтение)
#         return Habit.objects.filter(
#             models.Q(user=user) | models.Q(is_public=True, is_active=True)
#         ).distinct()
#
#     def perform_create(self, serializer):
#         """При создании проставляем пользователя"""
#         serializer.save(user=self.request.user)
#
#     def get_serializer_context(self):
#         """Передаём request в сериализатор для создания"""
#         context = super().get_serializer_context()
#         context.update({"request": self.request})
#         return context
#
#
# # class PublicHabitListView(viewsets.ReadOnlyModelViewSet):
# #     """Список публичных привычек (только чтение)"""
# #     authentication_classes = []
# #     serializer_class = HabitSerializer
# #     permission_classes = [AllowAny]
# #     pagination_class = HabitPagination
# #
# #     def get_queryset(self):
# #         return Habit.objects.filter(is_public=True, is_active=True)
# #
# #     def get_permissions(self):
# #         return [AllowAny()]
#
# # class PublicHabitListView(APIView):
# #     """Список публичных привычек (только чтение)"""
# #     authentication_classes = []
# #     permission_classes = [AllowAny]
# #
# #     # def get(self, request):
# #     #     habits = Habit.objects.filter(is_public=True, is_active=True)
# #     #     serializer = HabitSerializer(habits, many=True)
# #     #     return Response(serializer.data)
# #
# #     def get(self, request):
# #         print("=== PUBLIC HABITS REQUEST ===")
# #         print("User:", request.user)
# #         print("Is authenticated:", request.user.is_authenticated)
# #         print("Session:", request.session.keys())
# #         habits = Habit.objects.filter(is_public=True, is_active=True)
# #         serializer = HabitSerializer(habits, many=True)
# #         return Response(serializer.data)


from django.db import models
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

    def get_queryset(self):
        """Возвращаем привычки пользователя ИЛИ публичные."""
        user = self.request.user
        return Habit.objects.filter(
            models.Q(user=user) | models.Q(is_public=True, is_active=True)
        ).distinct()

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
