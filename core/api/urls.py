# Django & DRF
from django.urls import path

# App
from . import views


urlpatterns = [
    path('signup/', views.SignUpAPIView.as_view())
]
