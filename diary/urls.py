from django.urls import path

from .apps import DiaryConfig
from .views import EntryListView, EntryDetailView, EntryCreateView, EntryUpdateView, EntryDeleteView, HomePageView

app_name = DiaryConfig.name

urlpatterns = [
    path("", HomePageView.as_view(), name="index"),
    path('entry/', EntryListView.as_view(), name='entry_list'),
    path('entry/<int:pk>/', EntryDetailView.as_view(), name='entry_detail'),
    path('entry/new/', EntryCreateView.as_view(), name='entry_create'),
    path('entry/<int:pk>/edit/', EntryUpdateView.as_view(), name='entry_update'),
    path('entry/<int:pk>/delete/', EntryDeleteView.as_view(), name='entry_delete'),
]
