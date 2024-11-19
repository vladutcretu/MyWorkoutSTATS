# Django
from django.urls import path

# App
from fitness.views import (
    musclegroups,
    exercises,
    workouts,
    exercise_to_workout,
    workingsets,
    public_workouts,
    comments,
    analysis
)


urlpatterns = [
    # Muscle groups urls
    path('musclegroups/', musclegroups.view_musclegroups, name='musclegroups'),
    path('musclegroups/create/', musclegroups.create_musclegroups, name='create-musclegroup'),
    path('musclegroups/edit/<int:musclegroup_id>/', musclegroups.edit_musclegroups, name='edit-musclegroup'),
    path('musclegroups/delete/<int:musclegroup_id>/', musclegroups.delete_musclegroups, name='delete-musclegroup'),

    # Exercise urls
    path('exercises/', exercises.view_exercises, name='exercises'),
    path('exercises/create/', exercises.create_exercises, name='create-exercise'),
    path('exercises/edit/<int:exercise_id>/', exercises.edit_exercises, name='edit-exercise'),
    path('exercises/delete/<int:exercise_id>/', exercises.delete_exercises, name='delete-exercise'),
    path('exercises/collection/', exercises.collection_exercises, name='collection-exercise'),

    # Workout urls
    path('workouts/', workouts.view_workouts, name='workouts'),
    path('workouts/create/', workouts.create_workouts, name='create-workout'),
    path('workouts/import/<int:workout_id>/', workouts.import_workouts, name='import-workout'),
    path('workouts/edit/<int:workout_id>/', workouts.edit_workout, name='edit-workout'),
    path('workouts/delete/<int:workout_id>/', workouts.delete_workout, name='delete-workout'),
    path('workouts/view/<int:workout_id>/', workouts.view_private_workout, name='view-private-workout'),

    # Exercise to Workout urls
    path('workout/<int:workout_id>/select-exercise/', exercise_to_workout.select_exercise, name='select-exercise'),
    path('add-exercise/<int:exercise_id>/<int:workout_id>/', exercise_to_workout.add_exercise_to_workout, name='add-exercise'),
    path('remove-exercise/<int:exercise_id>/', exercise_to_workout.remove_exercise_from_workout, name='remove-exercise'),

    # Working sets urls
    path('sets/', workingsets.view_sets, name='sets'),
    path('create-set/<int:exercise_id>/<int:workout_id>/', workingsets.create_sets, name='create-set'),
    path('copy-set/<int:workingset_id>', workingsets.copy_sets, name='copy-set'),
    path('edit-set/<int:workingset_id>/', workingsets.edit_sets, name='edit-set'),
    path('delete-set/<int:workingset_id>/', workingsets.delete_sets, name='delete-set'),

    # Public workout urls
    path('public-workouts/', public_workouts.view_public_workouts, name='public-workouts'),
    path('public-workouts/view/<int:workout_id>/', public_workouts.view_public_workout, name='view-public-workout'),

    # Comments (and replies) to public workout urls
    path('public-workouts/view/<int:workout_id>/comment/create/', comments.create_comment_or_reply, name='create-comment'),
    path('public-workouts/view/<int:workout_id>/comment/reply/<int:parent_id>/', comments.create_comment_or_reply, name='create-reply'),
    path('public-workouts/view/<int:workout_id>/comment/<int:comment_id>/edit/', comments.edit_comment, name='edit-comment'),
    path('public-workouts/view/<int:workout_id>/comment/<int:comment_id>/delete/', comments.delete_comment, name='delete-comment'),
    path('public-workouts/view/<int:workout_id>/like/', comments.like_workout, name='like-workout'),

    # Analysis urls
    path('analysis/bodyweight/', analysis.analysis_bodyweight, name='analyze-bodyweight'),
    path('analysis/volume/', analysis.analysis_volume, name='analyze-volume'),
    path('get-volume-data/', analysis.get_volume_data, name='get-volume-data'),
    path('analysis/records/', analysis.analysis_records, name='analyze-records'),
    path('get-record-data/', analysis.get_record_data, name='get-record-data'),
]