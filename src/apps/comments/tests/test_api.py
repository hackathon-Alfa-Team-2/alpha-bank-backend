from datetime import datetime, timedelta

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

from src.apps.tasks.models import Task
from src.apps.comments.models import Comment
from src.apps.lms.models import LMS
from src.apps.users.models import CustomUser


class CommentAPITestCase(APITestCase):
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

        self.url_list = reverse(
            "api_v1:comments-list", kwargs={"task_id": self.task.id}
        )

        self.data = {"text_of_comment": "Test comment text"}

    def test_create_comment(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.supervisor_token.key
        )
        response = self.client.post(self.url_list, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(
            Comment.objects.get().text_of_comment, "Test comment text"
        )

    def test_create_invalid_comment(self):
        response = self.client.post(self.url_list, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_comments(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.supervisor_token.key
        )
        response = self.client.post(self.url_list)
        Comment.objects.create(
            text_of_comment="Comment 1",
            task=self.task,
            comment_author=self.supervisor,
        )
        Comment.objects.create(
            text_of_comment="Comment 2",
            task=self.task,
            comment_author=self.supervisor,
        )

        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_comment(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.employee_token.key
        )
        comment = Comment.objects.create(
            text_of_comment="Old text",
            task=self.task,
            comment_author=self.employee,
        )
        data = {"text_of_comment": "New text"}

        response = self.client.patch(
            "/api/v1/users/lms/tasks/{}/comments/{}/".format(
                self.task.id, comment.id
            ),
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.text_of_comment, "New text")

    def test_delete_comment(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.supervisor_token.key
        )
        comment = Comment.objects.create(
            text_of_comment="To be deleted",
            task=self.task,
            comment_author=self.supervisor,
        )

        response = self.client.delete(
            "/api/v1/users/lms/tasks/{}/comments/{}/".format(
                self.task.id, comment.id
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
