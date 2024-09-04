
from django.contrib import admin

from diary.models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'content', 'created_at', 'updated_at']
    search_fields = ['title', 'content']