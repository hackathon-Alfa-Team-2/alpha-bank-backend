from http import HTTPStatus

import pytest
from django.urls import reverse

from tests.pytest_tests.utils import mark_parametrize


class Test00Users:
    @pytest.mark.parametrize(*mark_parametrize.users_test_00_parametrize)
    def test_00_supervisor_can_make_request_to_users_endpoints(
        self,
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
        exp_status = HTTPStatus.OK
        response = supervisor_client.get(url)
        assert response.status_code == exp_status, (
            f"Статус ответа <{response.status_code}> не совпадает "
            f"с ожидаемым <{exp_status}>.",
        )

    @pytest.mark.parametrize(*mark_parametrize.users_test_01_parametrize)
    def test_01_supervisor_can_get_only_his_employees_list(
        self,
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
        assert response.data["count"] == employees_count, (
            "Ожидаемое количество сотрудников руководителя "
            "не совпадает с полученным.",
        )

    @pytest.mark.parametrize(*mark_parametrize.users_test_02_parametrize)
    def test_02_employee_can_make_request_to_user_me_endpoint(
        self,
        url_name,
        employee_client,
        employee,
    ):
        """Сотрудник может сделать запрос своей страницы."""
        url = reverse(url_name)
        exp_status = HTTPStatus.OK
        response = employee_client.get(url)
        assert response.status_code == exp_status, (
            f"Статус ответа <{response.status_code}> не совпадает "
            f"с ожидаемым <{exp_status}>.",
        )
        assert [response.data["first_name"], response.data["last_name"]] == [
            employee.first_name,
            employee.last_name,
        ], f"Получен ответ не не соответсвующий ожидаемому url:{url}."

    @pytest.mark.parametrize(*mark_parametrize.users_test_03_parametrize)
    def test_03_employee_can_not_make_request_to_users_list_and_detail(
        self,
        employee_client,
        url_name,
        user_id,
    ):
        """
        Запросы сотрудника.
        Сотрудник не может сделать запрос на:
            - Получение списка сотрудников
            - Получение детальной информации другого сотрудника
        """
        url = reverse(url_name, args=[user_id] if user_id else None)
        exp_status = HTTPStatus.FORBIDDEN
        response = employee_client.get(url)
        assert response.status_code == exp_status, (
            f"Статус ответа <{response.status_code}> не совпадает "
            f"с ожидаемым <{exp_status}>.",
        )

    def test_04_supervisor_can_not_make_request_to_another_supervisor_detail(
        self,
        supervisor_first_client,
        supervisor_second,
    ):
        """
        Руководитель не может сделать запрос детальной информации другого руководителя.
        """
        url = reverse("api_v1:users-detail", args=[supervisor_second.id])
        exp_status = HTTPStatus.NOT_FOUND
        response = supervisor_first_client.get(url)
        assert response.status_code == exp_status, (
            f"Статус ответа <{response.status_code}> не совпадает "
            f"с ожидаемым <{exp_status}>.",
        )

    @pytest.mark.parametrize(*mark_parametrize.users_test_05_parametrize)
    def test_05_supervisor_can_not_make_request_to_employee_not_subordinate(
        self,
        supervisor_client,
        employee,
    ):
        """
        Руководитель не может сделать запрос на чужого подчиненного.
        """
        url = reverse("api_v1:users-detail", args=[employee.id])
        exp_status = HTTPStatus.NOT_FOUND
        response = supervisor_client.get(url)
        assert response.status_code == exp_status, (
            f"Статус ответа <{response.status_code}> не совпадает "
            f"с ожидаемым <{exp_status}>.",
        )
