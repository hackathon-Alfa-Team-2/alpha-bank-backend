from datetime import datetime, timedelta

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

from src.apps.users.models import CustomUser


class LMSAPITestCase(APITestCase):
    def setUp(self):
        self.supervisor = CustomUser.objects.create(
            username="supervisor", password="testpassword"
        )
        self.supervisor.save()

        self.employee = CustomUser.objects.create(
            username="employee",
            password="testpassword",
            supervisor=self.supervisor,
        )
        self.employee.save()

        self.tomorrow = datetime.now() + timedelta(days=1)

        self.supervisor_token = Token.objects.create(user=self.supervisor)
        self.employee_token = Token.objects.create(user=self.employee)

        self.data = {
            "employee": self.employee.id,
            "supervisor": self.supervisor.id,
            "deadline": self.tomorrow,
        }

    def test_create_lms_as_supervisor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.supervisor_token.key
        )
        response = self.client.post(
            f"/api/v1/users/{self.employee.id}/lms/", self.data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
