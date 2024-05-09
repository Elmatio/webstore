from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings


class CustomUser(AbstractUser):
    username = models.CharField(max_length=250, blank=True, unique=True)
    middle_name = models.CharField(max_length=100, blank=True)
    born_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    last_name = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    born_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)