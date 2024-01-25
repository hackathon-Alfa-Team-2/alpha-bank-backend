from rest_framework import permissions
from rest_framework.request import Request

from src.apps.comments.models import Comment
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

    def has_object_permission(self, request: Request, view, obj: CustomUser):
        return (
            request.method in permissions.SAFE_METHODS
            and obj.supervisor == request.user
            or request.user.is_staff
        )


class IsAdminOrSupervisorOrLMSExecutor(TaskLMSBasePermission):
    """
    Права доступа для взаимодействия с ИПР:
        - List: Все пользователи
        - Retrieve: Руководитель и сотрудник связанные с этим ИПР и админ
        - Create: Руководитель и админ
        - Update/Delete: Руководитель связанный с этим ИПР и админ
    """

    def has_object_permission(self, request: Request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user == obj.employee_id
            or request.user == obj.supervisor_id
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


class IsAdminOrRelatedToTask(permissions.BasePermission):
    """
    Права доступа для взаимодействия с Задачами:
        - List: Все пользователи
        - Retrieve: Руководитель и сотрудник связанные с комментарием через
            задачу и админ
        - Create: Все пользователи
        - Update/Delete: Руководитель и Сотрудник связанный с этой задачей и
            админ
    """

    def has_object_permission(self, request, view, obj: Comment):
        return (
            obj.task.lms.supervisor == request.user
            or obj.task.lms.employee == request.user
            or request.user.is_staff
        )
