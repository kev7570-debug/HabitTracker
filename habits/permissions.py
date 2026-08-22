from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Права доступа:
    - Пользователь может редактировать/удалять только свои привычки
    - Публичные привычки доступны на чтение всем
    """

    def has_object_permission(self, request, view, obj):
        # Безопасные методы (GET, HEAD, OPTIONS) разрешены для всех
        if request.method in SAFE_METHODS:
            return True

        # Изменять/удалять можно только свою привычку
        return obj.user == request.user


class IsOwner(BasePermission):
    """
    Полный доступ только владельцу привычки.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    