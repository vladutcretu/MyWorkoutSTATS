from django.urls import path
from . import views


urlpatterns = [
    # Main page urls
    path('', views.main, name='main'),

    # Utility urls
    path('about/', views.page_about, name='about'),
    path('help/', views.page_help, name='help'),
    path('privacy/', views.page_privacy, name='privacy'),

    # Auth urls
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('recover/', views.user_account_recovery, name='recover'),
    path('change-password/', views.user_change_password, name='change-password'),
    path('delete-account/', views.user_delete_account, name='delete-account'),

    # User profile and account urls
    path('account/', views.user_account, name='account'),
    path('profile/<int:user_id>/', views.user_profile, name='profile'),
    path('profile/edit-profile/', views.user_profile_edit, name='edit-profile'),

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
    path('workouts/import/<int:workout_id>/', views.import_workouts, name='import-workout'),
    path('workouts/edit/<int:workout_id>/', views.edit_workout, name='edit-workout'),
    path('workouts/delete/<int:workout_id>/', views.delete_workout, name='delete-workout'),
    path('workouts/view/<int:workout_id>/', views.view_private_workout, name='view-private-workout'),

    # Exercise to Workout urls
    path('workout/<int:workout_id>/select-exercise/', views.select_exercise, name='select-exercise'),
    path('add-exercise/<int:exercise_id>/<int:workout_id>/', views.add_exercise_to_workout, name='add-exercise'),
    path('remove-exercise/<int:exercise_id>/', views.remove_exercise_from_workout, name='remove-exercise'),

    # Working sets urls
    path('sets/', views.view_workingsets, name='sets'),
    path('create-set/<int:exercise_id>/<int:workout_id>/', views.create_workingsets, name='create-workingset'),
    path('copy-set/<int:workingset_id>', views.copy_workingsets, name='copy-workingset'),
    path('edit-set/<int:workingset_id>/', views.edit_workingsets, name='edit-workingset'),
    path('delete-set/<int:workingset_id>/', views.delete_workingsets, name='delete-workingset'),

    # Public workout urls
    path('public-workouts/', views.view_public_workouts, name='public-workouts'),
    path('public-workouts/view/<int:workout_id>/', views.view_public_workout, name='view-public-workout'),

    # Comments (and replies) to public workout urls
    path('public-workouts/view/<int:workout_id>/comment/create/', views.create_comment_or_reply, name='create-comment'),
    path('public-workouts/view/<int:workout_id>/comment/reply/<int:parent_id>/', views.create_comment_or_reply, name='create-reply'),
    path('public-workouts/view/<int:workout_id>/comment/edit/<int:comment_id>/', views.edit_comment, name='edit-comment'),
    path('public-workouts/view/<int:workout_id>/comment/delete/<int:comment_id>/', views.delete_comment, name='delete-comment'),
    path('public-workouts/view/<int:workout_id>/like/', views.like_workout, name='like-workout'),

    # Analysis urls
    path('analysis/bodyweight/', views.analysis_bodyweight, name='analyze-bodyweight'),
    path('analysis/volume/', views.analysis_volume, name='analyze-volume'),
    path('get-volume-data/', views.get_volume_data, name='get-volume-data'),
    path('analysis/records/', views.analysis_records, name='analyze-records'),
    path('get-record-data/', views.get_record_data, name='get-record-data'),
]