from datetime import date, timedelta

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

from src.apps.users.models import CustomUser, Role
from src.apps.lms.models import LMS
from src.apps.tasks.models import Task


class TaskAPITestCase(APITestCase):
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

        self.lms = LMS.objects.create(
            employee=self.employee,
            supervisor=self.supervisor,
            deadline=self.tomorrow,
        )

        self.url_list = reverse(
            "api_v1:tasks-list",
            kwargs={"user_id": self.supervisor.id, "lms_id": self.lms.id},
        )

        self.data = {
            "name": "New Task",
            "deadline": self.tomorrow,
            "lms": self.lms,
        }

    def test_get_tasks_list(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.supervisor_token.key
        )
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.supervisor_token.key
        )
        response = self.client.post(self.url_list, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().name, "New Task")

    def test_update_task(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.supervisor_token.key
        )
        task = Task.objects.create(**self.data)
        url = reverse(
            "api_v1:tasks-detail",
            kwargs={
                "user_id": self.supervisor.id,
                "lms_id": self.lms.id,
                "pk": task.pk,
            },
        )
        data = {
            "name": "Updated Task",
            "description": "Updated Description",
            "deadline": self.tomorrow,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.name, "Updated Task")
        self.assertEqual(task.description, "Updated Description")

    def test_delete_task(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.supervisor_token.key
        )
        task = Task.objects.create(**self.data)
        url = reverse(
            "api_v1:tasks-detail",
            kwargs={
                "user_id": self.supervisor.id,
                "lms_id": self.lms.id,
                "pk": task.pk,
            },
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
