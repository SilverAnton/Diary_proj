from django import forms
from .models import Memory


class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ["entry", "reminder_date"]
        widgets = {
            "reminder_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
