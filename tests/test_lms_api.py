from datetime import date, timedelta

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

from src.apps.users.models import CustomUser, Role
from src.apps.lms.models import LMS


class LMSAPITestCase(APITestCase):
    def setUp(self):
        self.tomorrow = date.today() + timedelta(days=1)

        self.role = Role.objects.create(name="supervisor")

        self.supervisor = CustomUser.objects.create(
            username="supervisor", password="testpassword", role=self.role
        )

        self.employee = CustomUser.objects.create(
            username="employee",
            password="testpassword",
            supervisor=self.supervisor,
        )

        self.supervisor_token = Token.objects.create(user=self.supervisor)
        self.employee_token = Token.objects.create(user=self.employee)

        self.lms_data = {
            "supervisor": self.supervisor,
            "employee": self.employee,
            "name": "Test LMS",
            "description": "Test description",
            "deadline": self.tomorrow,
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

    def test_get_lms_list_as_supervisor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.supervisor_token.key
        )
        response = self.client.get(f"/api/v1/users/{self.employee.id}/lms/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
