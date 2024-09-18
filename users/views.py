from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.views import PasswordResetView

from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserUpdateForm, UserRecoveryForm
from users.models import User
import secrets
from django.contrib.auth import login
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    model = User
    template_name = "users/login.html"
    success_url = reverse_lazy("diary:index")

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active and user.auto_deactivated:
            user.is_active = True
            user.auto_deactivated = False
            user.save()
            messages.info(self.request, "Your account has been activated.")
        login(self.request, user)
        return redirect(self.get_success_url())


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        try:
            user.email_user(
                subject="Email Confirmation",
                message=f"Hello! Please confirm your email by following this link: {url}.",
            )
            messages.info(
                self.request, "Confirmation email sent. Please check your email."
            )
        except Exception as e:
            messages.error(self.request, f"Error sending email: {e}")
        return super().form_valid(form)


class UpdateFormView(UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("users:user_form")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    messages.success(request, "Your email has been confirmed. You can now log in.")
    return redirect(reverse("users:login"))


class UserPasswordResetView(PasswordResetView):
    form_class = UserRecoveryForm
    template_name = "users/recovery_form.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        if self.request.method == "POST":
            user_email = self.request.POST.get("email")
            user = User.objects.filter(email=user_email).first()
            if user:
                new_password = get_random_string(length=12)
                user.set_password(new_password)
                user.save()
                try:
                    user.email_user(
                        subject="Password Reset",
                        message=f"Hello! Your password has been reset. Here are your new login details:\n"
                        f"Email: {user_email}\n"
                        f"Password: {new_password}",
                    )
                    messages.info(
                        self.request,
                        "Password reset successfully. Please check your email.",
                    )
                except Exception as e:
                    messages.error(self.request, f"Error sending email: {e}")
                return HttpResponseRedirect(reverse("users:login"))
            else:
                messages.error(self.request, "Email address not found.")
        return super().form_valid(form)
