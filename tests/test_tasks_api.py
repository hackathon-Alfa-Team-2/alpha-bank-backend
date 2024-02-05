from datetime import date, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from src.apps.lms.models import LMS
from src.apps.tasks.models import Task
from src.apps.users.models import CustomUser, Role


class TaskAPITestCase(APITestCase):
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

        cls.lms = LMS.objects.create(
            employee=cls.employee,
            supervisor=cls.supervisor,
            deadline=cls.tomorrow,
        )

        cls.url_list = reverse(
            "api_v1:tasks-list",
            kwargs={"user_id": cls.employee.id, "lms_id": cls.lms.id},
        )

        cls.data = {
            "name": "New Task",
            "description": "Task description",
            "deadline": cls.tomorrow,
            "lms_id": cls.lms.id,
        }

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
                "user_id": self.employee.id,
                "lms_id": self.lms.id,
                "pk": task.pk,
            },
        )
        data = {
            "name": "Updated Task",
            "description": "Updated Description",
            "deadline": self.tomorrow,
        }
        response = self.client.patch(url, data)
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
                "user_id": self.employee.id,
                "lms_id": self.lms.id,
                "pk": task.pk,
            },
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
