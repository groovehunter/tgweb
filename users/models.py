
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

#import datetime
from django.utils.timezone import now

"""
class CustomUser(AbstractUser):

    dt_added    = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('users:profile', args=[self.username])
"""
