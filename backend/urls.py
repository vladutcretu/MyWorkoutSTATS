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

    # Workout urls
    path('workouts/', views.view_workouts, name='workouts'),
    path('workouts/create/', views.create_workouts, name='create-workout'),
    path('workouts/edit/<int:workout_id>/', views.edit_workout, name='edit-workout'),
    path('workouts/delete/<int:workout_id>/', views.delete_workout, name='delete-workout'),
    path('workouts/view/<int:workout_id>/', views.view_private_workout, name='view-private-workout'),

    # Exercise to Workout urls
    path('workout/<int:workout_id>/select-exercise/', views.select_exercise, name='select-exercise'),
    path('add-exercise-to-workout/<int:exercise_id>/<int:workout_id>/', views.add_exercise_to_workout, name='add-exercise-to-workout'),
    path('remove-exercise-from-workout/<int:exercise_id>/', views.remove_exercise_from_workout, name='remove-exercise-from-workout')
]