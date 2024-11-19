# Django
from django.contrib import admin

# App
from core.models import CustomUser


admin.site.register(CustomUser)