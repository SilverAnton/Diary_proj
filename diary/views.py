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


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["entries"] = Entry.objects.filter(user=self.request.user)
        else:
            context["entries"] = []
        return context


# Просмотр всех записей
class EntryListView(ListView):
    model = Entry
    template_name = "diary/entry_list.html"
    context_object_name = "entries"

    def get_queryset(self):
        queryset = Entry.objects.filter(user=self.request.user).order_by("-created_at")
        query = self.request.GET.get("query")  # Измените 'q' на 'query'
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
class EntryDetailView(DetailView):
    model = Entry
    template_name = "diary/entry_detail.html"


# Создание новой записи
class EntryCreateView(CreateView):
    model = Entry
    form_class = EntryForm
    template_name = "diary/entry_form.html"
    success_url = reverse_lazy("diary:entry_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Редактирование записи
class EntryUpdateView(UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = "diary/entry_form.html"
    success_url = reverse_lazy("diary:entry_list")


# Удаление записи
class EntryDeleteView(DeleteView):
    model = Entry
    template_name = "diary/entry_confirm_delete.html"
    success_url = reverse_lazy("diary:entry_list")
