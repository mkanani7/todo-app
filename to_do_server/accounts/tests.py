from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from todos.models import Todo


class TodoApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            username="user",
            password="password123",
        )
        self.client.force_authenticate(self.user)

    def test_user_can_login_and_create_and_list_todos(self):
        login_response = self.client.post(
            reverse("user-login"),
            {"email": "user@example.com", "password": "password123"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        payload = {
            "title": "Buy milk",
            "description": "For breakfast",
            "reminder_time": "2026-07-07T10:00:00Z",
        }

        response = self.client.post(reverse("todo-list"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(response.data["title"], "Buy milk")
        self.assertIn("reminder_time", response.data)

        list_response = self.client.get(reverse("todo-list"))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data[0]["title"], "Buy milk")

    def test_user_can_mark_todo_done_and_undone_and_update_it(self):
        todo = Todo.objects.create(user=self.user, title="Write report")

        response = self.client.patch(reverse("todo-toggle-done", args=[todo.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_done"])

        response = self.client.patch(reverse("todo-toggle-done", args=[todo.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_done"])

        update_response = self.client.patch(
            reverse("todo-detail", args=[todo.pk]),
            {"title": "Write final report", "description": "Ready"},
            format="json",
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["title"], "Write final report")

    def test_user_can_delete_todo(self):
        todo = Todo.objects.create(user=self.user, title="Delete me")

        response = self.client.delete(reverse("todo-detail", args=[todo.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(pk=todo.pk).exists())

    def test_jwt_token_endpoints_issue_and_accept_tokens(self):
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"email": "user@example.com", "password": "password123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data['access']}"
        )
        list_response = self.client.get(reverse("todo-list"))

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
