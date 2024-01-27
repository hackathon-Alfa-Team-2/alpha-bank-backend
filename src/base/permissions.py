from django.db.models import Q
from django.urls import resolve
from rest_framework import permissions
from rest_framework.request import Request

from src.apps.comments.models import Comment
from src.apps.tasks.models import Task
from src.apps.users.models import CustomUser


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


class IsAdminOrSupervisorOrLMSExecutor(permissions.BasePermission):
    """
    Права доступа для взаимодействия с ИПР:
        - List: Все пользователи
        - Retrieve: Руководитель и сотрудник связанные с этим ИПР и админ
        - Create: Руководитель и админ
        - Update/Delete: Руководитель связанный с этим ИПР и админ
    """

    def has_permission(self, request: Request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_supervisor
            or request.user.is_staff
        )

    def has_object_permission(self, request: Request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user == obj.employee_id
            or request.user == obj.supervisor_id
            or request.user.is_staff
        )


class IsAdminOrSupervisorOrTaskExecutor(permissions.BasePermission):
    """
    Права доступа для взаимодействия с Задачами:
        - List/Retrieve/Create/Update/Delete: Админ, Руководитель и сотрудник
            связанные с этой задачей через ИПР.
    """

    def has_permission(self, request: Request, view):
        from_path_user: CustomUser = CustomUser.objects.filter(
            id=resolve(request.path_info).kwargs["user_id"],
        ).first()
        return (
            request.method in permissions.SAFE_METHODS
            and request.user == from_path_user
            or request.user.is_supervisor
            and request.user == from_path_user.supervisor
            or request.user.is_staff
        )

    def has_object_permission(self, request: Request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user == obj.lms.employee
            or request.user == obj.lms.supervisor
            or request.user.is_staff
        )


class IsAdminOrRelatedToTask(permissions.BasePermission):
    """
    Права доступа для взаимодействия с Комментариями:
        - List/Create/Retrieve/Update/Delete: Админ, Руководитель и сотрудник
            связанные с комментарием через задачу и ИПР.
    """

    def has_permission(self, request, view):
        task_id = resolve(request.path_info).kwargs["task_id"]
        user = request.user
        task = Task.objects.select_related("lms").filter(
            Q(id=task_id, lms__employee=user)
            | Q(id=task_id, lms__supervisor=user)
        )
        if not task and not user.is_staff:
            return False
        return True

    def has_object_permission(self, request, view, obj: Comment):
        return (
            obj.task.lms.supervisor == request.user
            or obj.task.lms.employee == request.user
            or request.user.is_staff
        )
