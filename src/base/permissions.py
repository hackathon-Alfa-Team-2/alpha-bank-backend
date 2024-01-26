from django.urls import resolve
from rest_framework import permissions
from rest_framework.request import Request

from src.apps.users.models import CustomUser


class TaskLMSBasePermission(permissions.BasePermission):
    """
    Базовые права доступа для взаимодействия с ИПР и Задачами:
        - List: Все пользователи
        - Create: Руководитель и админ
    """

    def has_permission(self, request: Request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_supervisor
            or request.user.is_staff
        )


class IsAdminOrSupervisorReadOnly(permissions.BasePermission):
    """
    Права доступа для взаимодействия с Пользователями:
        - List/Retrieve: Руководитель и админ
        - Create: Только админ
        - Update/Delete: Только админ
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user.is_supervisor
            or request.user.is_staff
        )

    def has_object_permission(self, request: Request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            and obj.supervisor == request.user
            or request.user.is_staff
        )


class IsAdminOrSupervisorOrLMSExecutor(permissions.BasePermission):
    """
    Права доступа для взаимодействия с ИПР:
        - List/Retrieve/: Админ, руководитель и сотрудник
            связанные с этим ИПР
        - Create/Update/Delete: Админ и руководитель связанный с сотрудником.
    """

    def has_permission(self, request: Request, view):
        from_path_user: CustomUser = CustomUser.objects.filter(
            id=resolve(request.path_info).kwargs["user_id"],
        ).first()
        return (
            request.method in permissions.SAFE_METHODS
            and request.user == from_path_user
            or request.user == from_path_user.supervisor
            or request.user.is_staff
        )

    def has_object_permission(self, request: Request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user == obj.employee
            or request.user == obj.supervisor
            or request.user.is_staff
        )


class IsAdminOrSupervisorOrTaskExecutor(TaskLMSBasePermission):
    """
    Права доступа для взаимодействия с Задачами:
        - List: Все пользователи
        - Retrieve: Руководитель и сотрудник связанные с этой задачей и админ
        - Create: Руководитель и админ
        - Update/Delete: Руководитель связанный с этой задачей и админ
    """

    def has_object_permission(self, request: Request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user == obj.lms.employee
            or request.user == obj.lms.supervisor
            or request.user.is_staff
        )
