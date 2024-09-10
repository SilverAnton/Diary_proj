import os
from dotenv import load_dotenv
import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Memory

load_dotenv()


@shared_task
def send_memory_reminder(memory_id):
    memory = Memory.objects.get(id=memory_id)
    message = f"Reminder: {memory.entry.title}\n\n{memory.entry.content}"
    telegram_bot_token = settings.TELEGRAM_BOT_TOKEN
    telegram_chat_id = -1002111429474
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {"chat_id": telegram_chat_id, "text": message}
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        raise Exception(
            f"Telegram API request failed with status code {response.status_code}"
        )


@shared_task
def check_and_send_memories():
    now = timezone.now()
    upcoming_memories = Memory.objects.filter(
        reminder_date__lte=now, reminder_date__gte=now - timedelta(minutes=1)
    )
    for memory in upcoming_memories:
        send_memory_reminder(memory.id)
