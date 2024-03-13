from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_lazy_fixtures import lf

from tests.pytest_tests.conftest import (
    COUNT_MINOR_EMPLOYEES_SUPERVISOR_FIRST,
    COUNT_MINOR_EMPLOYEES_SUPERVISOR_SECOND,
)


@pytest.mark.parametrize(
    "url_name, supervisor_client, employee_id",
    (
        ("api_v1:users-list", lf("supervisor_first_client"), None),
        ("api_v1:users-list", lf("supervisor_second_client"), None),
        ("api_v1:users-me", lf("supervisor_first_client"), None),
        ("api_v1:users-me", lf("supervisor_second_client"), None),
        (
            "api_v1:users-detail",
            lf("supervisor_first_client"),
            lf("employee_first.id"),
        ),
        (
            "api_v1:users-detail",
            lf("supervisor_second_client"),
            lf("employee_second.id"),
        ),
    ),
)
def test_00_supervisor_can_make_request_to_users_endpoints(
    supervisor_client,
    url_name,
    employee_id,
):
    """
    Запросы руководителя.
    Руководитель может делать запросы на:
        - Получение своей страницы.
        - Получение списка своих сотрудников.
        - Получение детальной страницы своего сотрудника.
    """
    url = reverse(url_name, args=[employee_id] if employee_id else None)
    response = supervisor_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "supervisor_client, employees_count",
    (
        (
            lf("supervisor_first_client"),
            COUNT_MINOR_EMPLOYEES_SUPERVISOR_FIRST,
        ),
        (
            lf("supervisor_second_client"),
            COUNT_MINOR_EMPLOYEES_SUPERVISOR_SECOND,
        ),
    ),
)
def test_01_supervisor_can_get_only_his_employees_list(
    supervisor_client,
    employees_count,
    minor_employees,
):
    """
    Руководитель может сделать запрос на получение своих сотрудников.
    Ответ содержит только сотрудников руководителя сделавшего запрос.
    """
    url = reverse("api_v1:users-list")
    response = supervisor_client.get(url)
    assert response.data["count"] == employees_count


@pytest.mark.parametrize(
    "url_name, employee_client, employee",
    (
        (
            "api_v1:users-me",
            lf("employee_first_client"),
            lf("employee_first"),
        ),
        (
            "api_v1:users-me",
            lf("employee_second_client"),
            lf("employee_second"),
        ),
    ),
)
def test_02_employee_can_make_request_to_user_me_endpoint(
    url_name, employee_client, employee
):
    """Сотрудник может сделать запрос своей страницы."""
    url = reverse(url_name)
    response = employee_client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert [response.data["first_name"], response.data["last_name"]] == [
        employee.first_name,
        employee.last_name,
    ]


@pytest.mark.parametrize(
    "url_name, employee_client, user_id",
    (
        (
            "api_v1:users-list",
            lf("employee_first_client"),
            None,
        ),
        (
            "api_v1:users-list",
            lf("employee_second_client"),
            None,
        ),
        (
            "api_v1:users-detail",
            lf("employee_first_client"),
            lf("employee_second.id"),
        ),
        (
            "api_v1:users-detail",
            lf("employee_first_client"),
            lf("supervisor_first.id"),
        ),
        (
            "api_v1:users-detail",
            lf("employee_second_client"),
            lf("employee_first.id"),
        ),
        (
            "api_v1:users-detail",
            lf("employee_second_client"),
            lf("supervisor_second.id"),
        ),
    ),
)
def test_03_employee_can_not_make_request_to_users_list_and_detail(
    employee_client, url_name, user_id
):
    """
    Запросы сотрудника.
    Сотрудник не может сделать запрос на:
        - Получение списка сотрудников
        - Получение детальной информации другого сотрудника
    """
    url = reverse(url_name, args=[user_id] if user_id else None)
    response = employee_client.get(url)
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_04_supervisor_can_not_make_request_to_another_supervisor_detail(
    supervisor_first_client, supervisor_second
):
    """
    Руководитель не может сделать запрос детальной информации другого руководителя.
    """
    url = reverse("api_v1:users-detail", args=[supervisor_second.id])
    response = supervisor_first_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    "supervisor_client, employee",
    (
        (lf("supervisor_first_client"), lf("employee_second")),
        (lf("supervisor_second_client"), lf("employee_first")),
    ),
)
def test_05_supervisor_can_not_make_request_to_employee_not_subordinate(
    supervisor_client, employee
):
    url = reverse("api_v1:users-detail", args=[employee.id])
    response = supervisor_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
