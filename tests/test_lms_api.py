from datetime import date, timedelta

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from src.apps.lms.models import LMS
from src.apps.users.models import CustomUser, Role


class LMSAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tomorrow = date.today() + timedelta(days=1)

        cls.role = Role.objects.create(name="supervisor")

        cls.supervisor = CustomUser.objects.create(
            username="supervisor", password="testpassword", role=cls.role
        )

        cls.employee = CustomUser.objects.create(
            username="employee",
            password="testpassword",
            supervisor=cls.supervisor,
        )

        cls.supervisor_token = Token.objects.create(user=cls.supervisor)
        cls.employee_token = Token.objects.create(user=cls.employee)

        cls.lms_data = {
            "supervisor": cls.supervisor,
            "employee": cls.employee,
            "name": "Test LMS",
            "description": "Test description",
            "deadline": cls.tomorrow,
        }

    def test_create_lms_as_supervisor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.supervisor_token.key
        )
        response = self.client.post(
            f"/api/v1/users/{self.employee.id}/lms/", self.lms_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lms_as_employee(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.employee_token.key
        )
        response = self.client.post(
            f"/api/v1/users/{self.employee.id}/lms/", self.lms_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_lms_as_supervisor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.supervisor_token.key
        )
        lms = LMS.objects.create(**self.lms_data)
        new_deadline = self.tomorrow + timedelta(days=10)
        data = {"deadline": new_deadline}
        response = self.client.patch(
            f"/api/v1/users/{self.employee.id}/lms/{lms.id}/",
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lms_as_employee(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.employee_token.key
        )
        lms = LMS.objects.create(**self.lms_data)
        response = self.client.patch(
            f"/api/v1/users/{self.employee.id}/lms/{lms.id}/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lms_as_supervisor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.supervisor_token.key
        )
        lms = LMS.objects.create(**self.lms_data)
        response = self.client.delete(
            f"/api/v1/users/{self.employee.id}/lms/{lms.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lms_as_employee(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.employee_token.key
        )
        lms = LMS.objects.create(**self.lms_data)
        response = self.client.delete(
            f"/api/v1/users/{self.employee.id}/lms/{lms.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
