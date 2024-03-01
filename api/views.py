from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.models import Workout, WorkoutExercise, MuscleGroup, Exercise, WorkingSet
from .serializers import WorkoutSerializer, WorkoutExerciseSerializer, MuscleGroupSerializer, ExerciseSerializer, WorkingSetSerializer


@api_view(['GET'])
def get_workouts(request):
    workouts = Workout.objects.all()
    serializer = WorkoutSerializer(workouts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_workout_exercises(request):
    workout_exercises = WorkoutExercise.objects.all()
    serializer = WorkoutExerciseSerializer(workout_exercises, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_musclegroup(request):
    musclegroup = MuscleGroup.objects.all()
    serializer = MuscleGroupSerializer(musclegroup, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_exercises(request):
    exercises = Exercise.objects.all()
    serializer = ExerciseSerializer(exercises, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_workingsets(request):
    workingsets = WorkingSet.objects.all()
    serializer = WorkingSetSerializer(workingsets, many=True)
    return Response(serializer.data)
