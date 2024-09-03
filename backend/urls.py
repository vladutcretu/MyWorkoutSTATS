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
    path('change-password/', views.user_change_password, name='change-password'),

    # User profile and account urls
    path('profile/<int:user_id>/', views.user_profile, name='profile'),
    path('edit-profile/', views.user_profile_edit, name='edit-profile'),

    # Muscle groups urls
    path('musclegroups/', views.view_musclegroups, name='musclegroups'),
    path('musclegroups/create/', views.create_musclegroups, name='create-musclegroup'),
    path('musclegroups/edit/<int:musclegroup_id>/', views.edit_musclegroups, name='edit-musclegroup'),
    path('musclegroups/delete/<int:musclegroup_id>/', views.delete_musclegroups, name='delete-musclegroup'),

    # Exercise urls
    path('exercises/', views.view_exercises, name='exercises'),
    path('exercises/create', views.create_exercises, name='create-exercise'),
    path('exercises/edit/<int:exercise_id>/', views.edit_exercises, name='edit-exercise'),
    path('exercises/delete/<int:exercise_id>/', views.delete_exercises, name='delete-exercise'),
]