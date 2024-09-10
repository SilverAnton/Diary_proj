from users.models import User
from diary.models import Entry

from django.db import models
from django.utils import timezone


class Memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    reminder_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.reminder_date:
            self.reminder_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reminder for {self.entry.title} on {self.reminder_date}"

    class Meta:
        verbose_name = "Memory"
        verbose_name_plural = "Memories"
