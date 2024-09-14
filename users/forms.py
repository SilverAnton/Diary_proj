from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordResetForm,
)
from users.models import User
from django.forms import BooleanField


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.fields.items():

            if isinstance(v, BooleanField):
                v.widget.attrs["class"] = "form-check-input"
            else:
                v.widget.attrs["class"] = "form-control"


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2", "telegram_chat_id"]


class UserUpdateForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ["email", "phone", "avatar", "country", "telegram_chat_id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()


class UserRecoveryForm(StyleFormMixin, PasswordResetForm):
    class Meta:
        model = User
        fields = ("email",)
