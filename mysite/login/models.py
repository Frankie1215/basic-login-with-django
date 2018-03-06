from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    verified = models.BooleanField(default=False)
    verify_uuid = models.CharField(max_length=255, null=False, blank=False)
