from http import HTTPStatus

import pytest
from django.urls import reverse

from tests.pytest_tests.utils import mark_parametrize


class Test01LMS:
    POST_LMS_DATA = {
        "name": "employee_1_lms",
        "description": "Post_lms_employee_1",
        "is_active": True,
        "deadline": "2030-03-20",
        "status": "in_progress",
        "skill_assessment_before": 2,
        "skill_assessment_after": 5,
    }
    PATCH_LMS_DATA = {
        "name": "patch_employee_1_lms",
        "is_active": False,
        "skill_assessment_after": 4,
    }

    def test_00_supervisor_can_get_lms_detail_your_subordinate(
        self,
        supervisor_first_client,
        lms_first,
        employee_first,
    ):
        """Руководитель может просматривать ИПР своего подчиненного."""
        url = reverse(
            "api_v1:lms-detail", args=[employee_first.id, lms_first.id]
        )
        exp_status = HTTPStatus.OK
        response = supervisor_first_client.get(url)
        assert response.status_code == exp_status, (
            f"Статус ответа <{response.status_code}> не совпадает "
            f"с ожидаемым <{exp_status}>.",
        )
        assert (
            response.data["name"] == lms_first.name
        ), "Ожидаемое имя ИПР отличается от полученного."
        assert (
            response.data["description"] == lms_first.description
        ), "Ожидаемое описание ИПР отличается от полученного."

    @pytest.mark.parametrize(*mark_parametrize.lms_test_01_parametrize)
    def test_01_supervisor_can_get_lms_list_your_subordinate(
        self,
        supervisor_client,
        employee_id,
        lms_count,
        minor_lms,
    ):
        """Руководитель может получить список ИПР своих сотрудников."""
        url = reverse("api_v1:lms-list", args=[employee_id])
        exp_status = HTTPStatus.OK
        response = supervisor_client.get(url)
        assert response.status_code == exp_status, (
            f"Статус ответа <{response.status_code}> не совпадает "
            f"с ожидаемым <{exp_status}>.",
        )
        assert (
            len(response.data) == lms_count
        ), "Ожидаемое количество ИПР не совпадает с полученным."

    def test_02_supervisor_can_post_lms_your_subordinate(
        self,
        supervisor_first,
        supervisor_first_client,
        employee_first,
    ):
        url = reverse("api_v1:lms-list", args=[employee_first.id])
        exp_status = HTTPStatus.CREATED
        response = supervisor_first_client.post(url, data=self.POST_LMS_DATA)
        assert response.status_code == exp_status, (
            f"Статус ответа <{response.status_code}> не совпадает "
            f"с ожидаемым <{exp_status}>.",
        )
        assert (
            response.data.get("name") == self.POST_LMS_DATA["name"]
        ), "Полученное имя ИПР не совпадает с ожидаемым."
        assert response.data.get("supervisor") == supervisor_first.id, (
            f'Идентификатор руководителя {response.data.get("supervisor")} '
            f"не совпадает с ожидаемым <{supervisor_first.id}>"
        )
        assert response.data.get("employee_id") == employee_first.id, (
            f'Идентификатор сотрудника <{response.data.get("employee_id")}> '
            f"не совпадает с ожидаемым <{employee_first.id}>"
        )

    def test_03_supervisor_can_patch_lms_your_subordinate(
        self,
        lms_first,
        supervisor_first_client,
        employee_first,
    ):
        """Руководитель может редактировать ИПР своего подчиненного."""
        url = reverse(
            "api_v1:lms-detail", args=[employee_first.id, lms_first.id]
        )
        exp_status = HTTPStatus.OK
        response = supervisor_first_client.patch(url, data=self.PATCH_LMS_DATA)
        assert response.status_code == exp_status, (
            f"Статус ответа <{response.status_code}> не совпадает "
            f"с ожидаемым <{exp_status}>.",
        )
        assert (
            response.data.get("name") == self.PATCH_LMS_DATA["name"]
        ), "Полученное имя ИПР не совпадает с ожидаемым."
        assert (
            response.data.get("skill_assessment_after")
            == self.PATCH_LMS_DATA["skill_assessment_after"]
        ), "Полученная оценка навыка ИПР не совпадает с ожидаемым."
        assert (
            response.data.get("is_active") == self.PATCH_LMS_DATA["is_active"]
        ), "Полученный флаг активности ИПР не совпадает с ожидаемым."

    def test_04_supervisor_can_delete_lms_your_subordinate(
        self,
        lms_first,
        supervisor_first_client,
        employee_first,
    ):
        """Руководитель может удалить ИПР своего подчиненного."""
        url = reverse(
            "api_v1:lms-detail", args=[employee_first.id, lms_first.id]
        )
        exp_status = HTTPStatus.NO_CONTENT
        response = supervisor_first_client.delete(
            url,
            data=self.PATCH_LMS_DATA,
        )
        assert response.status_code == exp_status, (
            f"Статус ответа <{response.status_code}> не совпадает "
            f"с ожидаемым <{exp_status}>.",
        )
