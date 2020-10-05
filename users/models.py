from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True,
                                max_length=20,
                                blank=False,
                                null=False)
    first_name = models.CharField(max_length=80,
                                  blank=False,
                                  null=False)

    def __str__(self):
        return self.username
