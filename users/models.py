from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    phone = models.CharField(max_length=100, verbose_name="phone")
    avatar = models.ImageField(
        upload_to="users/", verbose_name="avatar", null=True, blank=True
    )
    country = models.CharField(
        max_length=150, verbose_name="country", null=True, blank=True
    )
    token = models.CharField(
        max_length=100, verbose_name="token", null=True, blank=True
    )
    is_active = models.BooleanField(default=True, verbose_name="is_active")
    telegram_chat_id = models.CharField(max_length=155, verbose_name="telegram_chat_id", null=True, blank=True)
    auto_deactivated = models.BooleanField(default=False, verbose_name="deactivated", null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_change_user_status", "Can change user status"),
        ]
