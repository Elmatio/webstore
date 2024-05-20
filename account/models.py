from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings


class CustomUser(AbstractUser):
    username = models.CharField(max_length=250, blank=True, unique=True)
    middle_name = models.CharField(max_length=100, blank=True)
    passport = models.CharField(max_length=10, blank=True)
    born_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
