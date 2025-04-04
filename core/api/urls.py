# Django & DRF
from django.urls import path

# App
from . import views


urlpatterns = [
    # Auth urls
    path("signup/", views.SignUpAPIView.as_view()),
    path("login/", views.LogInAPIView.as_view()),
    # User profile and account urls
    path("profile/", views.CustomUserAPIView.as_view()),
]
