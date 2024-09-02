from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """Model Custom for User to achieve profile feature"""
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(null=True, default='default.jpg')
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=300, blank=True, null=True)
    instagram_url = models.URLField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username