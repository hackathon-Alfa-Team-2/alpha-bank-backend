from datetime import datetime, timedelta

from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from src.apps.tasks.models import Task
from src.apps.comments.models import Comment
from src.apps.lms.models import LMS
from src.apps.users.models import CustomUser


class CommentAPITestCase(APITestCase):
    def setUp(self):
        self.supervisor = CustomUser.objects.create(
            username="user_1", password="testpassword"
        )
        self.supervisor.save()
        self.employee = CustomUser.objects.create(
            username="employee", password="testpassword"
        )
        self.employee.save()

        tomorrow = datetime.now() + timedelta(days=1)

        self.lms = LMS.objects.create(
            employee=self.employee,
            supervisor=self.supervisor,
            deadline=tomorrow,
        )
        self.lms.save()
        self.task = Task.objects.create(lms=self.lms, deadline=tomorrow)
        self.task.save()

        self.supervisor_token = Token.objects.create(user=self.supervisor)
        self.employee_token = Token.objects.create(user=self.employee)

        self.data = {"text_of_comment": "Test comment text"}

    def test_create_comment(self):
        client = APIClient()
        client.credentials(
            HTTP_AUTHORIZATION="Token " + self.supervisor_token.key
        )
        response = self.client.post(
            "/api/v1/users/lms/tasks/1/comments/".format(self.task), self.data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(
            Comment.objects.get().text_of_comment, "Test comment text"
        )

    def test_create_invalid_comment(self):
        response = self.client.post(
            "/api/v1/users/lms/tasks/1/comments/", self.data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
