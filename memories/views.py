from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Memory
from .forms import MemoryForm
from django.http import JsonResponse
from django.urls import reverse


class MemoryCreateView(CreateView):
    model = Memory
    form_class = MemoryForm
    template_name = "memories/memory_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})
        return response

    def form_invalid(self, form):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            import logging

            logger = logging.getLogger(__name__)
            logger.error("Form errors: %s", form.errors)
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("diary:index")


class MemoryUpdateView(UpdateView):
    model = Memory
    form_class = MemoryForm
    template_name = "memories/memory_form.html"
    success_url = reverse_lazy("diary:entry_list")


class MemoryDeleteView(DeleteView):
    model = Memory
    template_name = "memories/memory_confirm_delete.html"
    success_url = reverse_lazy("diary:entry_list")
