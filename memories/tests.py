from django.test import TestCase
from django.urls import reverse
from .models import Memory
from diary.models import Entry
from users.models import User
from django.utils import timezone


class MemoryCRUDTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.client.force_login(self.user)

        self.entry = Entry.objects.create(
            user=self.user, title="Test Entry", content="This is a test entry content."
        )

        self.memory = Memory.objects.create(
            user=self.user, entry=self.entry, reminder_date=timezone.now()
        )

    def test_memory_create(self):
        data = {"entry": self.entry.id, "reminder_date": timezone.now()}
        response = self.client.post(reverse("memories:memory_create"), data)
        self.assertEqual(
            response.status_code, 302
        )  # Ожидаем перенаправление после создания
        self.assertEqual(Memory.objects.count(), 2)

    def test_memory_update(self):
        new_date = timezone.now() + timezone.timedelta(days=1)
        data = {"entry": self.entry.id, "reminder_date": new_date}
        response = self.client.post(
            reverse("memories:memory_update", args=[self.memory.id]), data
        )
        self.memory.refresh_from_db()
        self.assertEqual(self.memory.reminder_date, new_date)
        self.assertEqual(
            response.status_code, 302
        )  # Ожидаем перенаправление после обновления

    def test_memory_delete(self):
        response = self.client.post(
            reverse("memories:memory_delete", args=[self.memory.id])
        )
        self.assertEqual(
            response.status_code, 302
        )  # Ожидаем перенаправление после удаления
        self.assertEqual(Memory.objects.count(), 0)
