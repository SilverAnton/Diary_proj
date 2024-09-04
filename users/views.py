import string

from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.views import PasswordResetView

from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, UpdateView


from users.forms import UserRegisterForm, UserUpdateForm, UserRecoveryForm
from users.models import User
import secrets


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        user.email_user(
            subject="Подтверждение почты",
            message=f"Привет, подтвердите свой email по ссылке {url}, для завершения регистрации",

        )
        return super().form_valid(form)


class UpdateFormView(UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:user_form')

    def get_object(self, queryset=None):
        return self.request.user


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


#def make_random_password():
#character = string.ascii_letters + string.digits
#password = "".join(secrets.choice(character) for i in range(12))

# return password


class UserPasswordResetView(PasswordResetView):
    form_class = UserRecoveryForm
    template_name = 'users/recovery_form.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if self.request.method == 'POST':
            user_email = self.request.POST.get('email')
            user = User.objects.filter(email=user_email).first()
            if user:
                new_password = get_random_string(length=12)
                user.set_password(new_password)
                user.save()
                try:
                    user.email_user(
                        subject="Восстановление пароля",
                        message=f"Здравствуйте! Ваш пароль для доступа на наш сайт изменен:\n"
                                f"Данные для входа:\n"
                                f"Email: {user_email}\n"
                                f"Пароль: {new_password}"
                    )
                except Exception:
                    print(f'Ошибка пр отправке письма, {user.email}')
                return HttpResponseRedirect(reverse('users:login'))
            else:
                # Обработка неверного email-адреса
                context = {'error_message': 'Такой email не зарегистрирован.'}
                return render(self.request, 'users/recovery_form.html', context)
