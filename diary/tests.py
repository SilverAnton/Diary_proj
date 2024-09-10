from django.test import TestCase
from django.urls import reverse
from .models import Entry
from users.models import User


class EntryCRUDTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.client.force_login(self.user)

        self.entry = Entry.objects.create(
            user=self.user, title="Test Entry", content="This is a test entry content."
        )

    def test_entry_list(self):
        response = self.client.get(reverse("diary:entry_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Entry")

    def test_entry_detail(self):
        response = self.client.get(reverse("diary:entry_detail", args=[self.entry.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Entry")

    def test_entry_create(self):
        data = {"title": "New Test Entry", "content": "Content of the new test entry."}
        response = self.client.post(reverse("diary:entry_create"), data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertEqual(Entry.objects.count(), 2)

    def test_entry_update(self):
        data = {
            "title": "Updated Test Entry",
            "content": "Updated content of the test entry.",
        }
        response = self.client.post(
            reverse("diary:entry_update", args=[self.entry.id]), data
        )
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.title, "Updated Test Entry")
        self.assertEqual(response.status_code, 302)

    def test_entry_delete(self):
        response = self.client.post(reverse("diary:entry_delete", args=[self.entry.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.count(), 0)
