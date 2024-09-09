
from django.contrib import admin

from memories.models import Memory


@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'entry', 'reminder_date']
    search_fields = ['user', 'entry', 'reminder_date']
