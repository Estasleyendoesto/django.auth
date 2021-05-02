from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('profile', kwargs={'username': self.username})
