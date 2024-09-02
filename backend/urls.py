from django.urls import path
from . import views

urlpatterns = [
    # Main page urls
    path('', views.main, name='main'),

    # Auth urls
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('recover/', views.user_account_recovery, name='recover'),
]