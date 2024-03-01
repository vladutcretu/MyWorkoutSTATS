from django.urls import path
from . import views

urlpatterns = [
    # Auth & Security urls
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),

    # Main page urls
    path('', views.homePage, name='home'),

    # User account urls
    path('account/', views.userAccount, name='account'),

    # Workout urls: CRUD workout and all workout related actions
    path('workouts/', views.workouts, name='workouts'),
    path('view_workout/<int:workout_id>/', views.view_workout, name='view_workout'),
    path('create_workout/', views.create_workout, name='create_workout'),
    path('import_workout/<int:workout_id>/', views.import_workout, name='import_workout'),
    path('edit_workout/<int:workout_id>/', views.edit_workout, name='edit_workout'),
    path('delete_workout/<int:workout_id>/', views.delete_workout, name='delete_workout'),
    path('add_exercise/<int:workout_id>/', views.add_exercise, name='add_exercise'),
    path('add_exercise_to_workout/<int:exercise_id>/<int:workout_id>/', views.add_exercise_to_workout, name='add_exercise_to_workout'),
    path('delete_exercise_from_workout/<int:exercise_id>/', views.delete_exercise_from_workout, name='delete_exercise_from_workout'),
    path('add_workingset_to_exercise/<int:exercise_id>/<int:workout_id>/', views.add_workingset_to_exercise, name='add_workingset_to_exercise'),
    path('delete_workingset_from_exercise/<int:workingset_id>/', views.delete_workingset_from_exercise, name='delete_workingset_from_exercise'),
    path('edit_workingset/<int:workingset_id>/', views.edit_workingset, name='edit_workingset'),

    # Muscle groups urls
    path('musclegroups/', views.musclegroups, name='musclegroups'),
    path('create_musclegroup/', views.create_musclegroup, name='create_musclegroup'),
    path('delete_musclegroup/<int:musclegroup_id>/', views.delete_musclegroup, name='delete_musclegroup'),

    # Exercise urls
    path('exercises/', views.exercises, name='exercises'),
    path('create_exercise/', views.create_exercise, name='create_exercise'),
    path('delete_exercise/<int:exercise_id>/', views.delete_exercise, name='delete_exercise'),

    # Analysis urls
    path('bodyweight_analysis/', views.bodyweight_analysis, name='bodyweight_analysis'),
    path('exercise_analysis/', views.exercise_analysis, name='exercise_analysis'),
    path('exercise_records/', views.exercise_records, name='exercise_records'),

    # Community urls
    path('public_workouts/', views.public_workouts, name='public_workouts'),
    path('about_help/', views.about_help, name='about_help'),
]


