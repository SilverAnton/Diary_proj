from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    TemplateView,
)
from .models import Entry
from .forms import EntryForm, SearchForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from random import sample
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            entries = Entry.objects.filter(user=self.request.user)
            context["entries"] = entries
            if entries.exists():
                random_entries = sample(list(entries), min(3, entries.count()))
                context["random_entries"] = random_entries
            context["has_telegram_chat_id"] = bool(self.request.user.telegram_chat_id)
        else:
            context["entries"] = []
            context["random_entries"] = []
            context["has_telegram_chat_id"] = False
        return context

# Просмотр всех записей
class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = "diary/entry_list.html"
    context_object_name = "entries"

    def get_queryset(self):
        queryset = Entry.objects.filter(user=self.request.user).order_by("-created_at")
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET)
        return context


# Просмотр одной записи
class EntryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Entry
    template_name = "diary/entry_detail.html"

    def test_func(self):
        entry = self.get_object()
        return entry.user == self.request.user


# Создание новой записи
class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = "diary/entry_form.html"
    success_url = reverse_lazy("diary:entry_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Редактирование записи
class EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = "diary/entry_form.html"
    success_url = reverse_lazy("diary:entry_list")

    def test_func(self):
        entry = self.get_object()
        return entry.user == self.request.user


# Удаление записи
class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry
    template_name = "diary/entry_confirm_delete.html"
    success_url = reverse_lazy("diary:entry_list")

    def test_func(self):
        entry = self.get_object()
        return entry.user == self.request.user
