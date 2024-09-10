from django.urls import path

from .apps import MemoriesConfig
from .views import MemoryCreateView, MemoryUpdateView, MemoryDeleteView

app_name = MemoriesConfig.name

urlpatterns = [
    path("create/", MemoryCreateView.as_view(), name="memory_create"),
    path("memory/<int:pk>/edit/", MemoryUpdateView.as_view(), name="memory_update"),
    path("memory/<int:pk>/delete/", MemoryDeleteView.as_view(), name="memory_delete"),
]
