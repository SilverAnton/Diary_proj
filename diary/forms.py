from django import forms

from users.forms import StyleFormMixin
from .models import Entry


class EntryForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(
        label="Search",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search..."}
        ),
    )
