from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class UserCRUDTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.client.force_login(self.user)

        # Определяем URL для CRUD операций
        self.create_url = reverse("users:register")
        self.update_url = reverse("users:user_form")
        self.password_reset_url = reverse("users:recovery_form")

    def test_create_user(self):
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "testuser@example.com")

    def test_update_user(self):
        data = {"email": "updatedemail@example.com", "phone": "1234567890"}
        response = self.client.post(self.update_url, data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updatedemail@example.com")
        self.assertEqual(
            response.status_code, 302
        )  # Ожидаем перенаправление после обновления
