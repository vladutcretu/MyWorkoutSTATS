from rest_framework import serializers
from backend.models import Workout, WorkoutExercise, MuscleGroup, Exercise, WorkingSet


class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = ['id', 'user', 'name']


class WorkingSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingSet
        fields = ['id', 'user', 'workout', 'exercise', 'weight', 'repetitions', 'distance', 'time']


class ExerciseSerializer(serializers.ModelSerializer):
    musclegroup = MuscleGroupSerializer()
    workingsets = WorkingSetSerializer(many=True)

    class Meta:
        model = Exercise
        fields = ['id', 'user', 'musclegroup', 'name', 'workingsets']


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer()

    class Meta:
        model = WorkoutExercise
        fields = ['id', 'workout', 'exercise', 'order']


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = Workout
        fields = ['id', 'user', 'created', 'name', 'bodyweight', 'public', 'exercises', 'note']
