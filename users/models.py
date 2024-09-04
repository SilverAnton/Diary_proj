from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    phone = models.CharField(max_length=100, verbose_name='phone')
    avatar = models.ImageField(upload_to='users/', verbose_name='avatar', null=True, blank=True)
    country = models.CharField(max_length=150, verbose_name='country', null=True, blank=True)
    token = models.CharField(max_length=100, verbose_name='token', null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

