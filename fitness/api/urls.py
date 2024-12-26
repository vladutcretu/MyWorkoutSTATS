# Django & DRF
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# App
from . import views


router = DefaultRouter()
router.register(r'musclegroups', views.MuscleGroupAPIView, basename='musclegroups')


urlpatterns = [
    path('', include(router.urls))
]