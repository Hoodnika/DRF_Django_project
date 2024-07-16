from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    message = 'Ошибка в правах доступа'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moder').exists()


class IsOwner(BasePermission):
    message = 'Adding customers not allowed'

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsMe(BasePermission):
    message = 'Это не твой профиль, ты куда лезешь'

    def has_object_permission(self, request, view, obj):
        return obj == request.user
