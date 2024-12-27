# Django & DRF
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

# App
from fitness.models import MuscleGroup, Exercise, Workout, WorkoutExercise, WorkingSet
from .serializers import MuscleGroupSerializer, ExerciseSerializer, WorkoutSerializer, WorkoutExerciseSerializer, WorkingSetSerializer
from .permissions import IsOwner


class MuscleGroupAPIView(viewsets.ModelViewSet):
    """API endpoint for the muscle groups (CRUD operations)"""
    serializer_class = MuscleGroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Only allow access to appropriate (owned) object(s)"""
        return MuscleGroup.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user field to the currently authenticated (and requested) user."""
        serializer.save(user=self.request.user)


class ExerciseAPIView(viewsets.ModelViewSet):
    """API endpoint for the exercises (CRUD operations)"""
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Only allow access to appropriate (owned) object(s)"""
        return Exercise.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user field to the currently authenticated (and requested) user."""
        serializer.save(user=self.request.user)


class WorkoutAPIView(viewsets.ModelViewSet):
    """API endpoint for the workouts (CRUD operations)"""
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Only allow access to appropriate (owned) object(s)"""
        return Workout.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user field to the currently authenticated (and requested) user."""
        serializer.save(user=self.request.user)


class WorkoutExerciseAPIView(viewsets.ViewSet):
    serializer_class = WorkoutExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Only allow access to appropriate (owned) object(s)"""
        return WorkoutExercise.objects.filter(workout__user=self.request.user)

    def list(self, request):
        """List (GET) all workout - exercise relationships for the requested user."""
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Add (POST) an exercise to workout."""
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """Set order parameter value"""
        workout = serializer.validated_data['workout']
        order = WorkoutExercise.objects.filter(workout=workout).count() + 1
        serializer.save(order=order)

    def destroy(self, request, pk=None):
        """Remove (DELETE) an exercise from workout."""
        try:
            workout_exercise = WorkoutExercise.objects.get(id=pk, workout__user=request.user)
        except WorkoutExercise.DoesNotExist:
            return Response({"detail": "Can not delete an object that is not owned by you."}, status=status.HTTP_404_NOT_FOUND)

        workout_exercise.delete()
        return Response({"detail": "Exercise has been successfully removed from workout."}, status=status.HTTP_204_NO_CONTENT)


class WorkingSetAPIView(viewsets.ModelViewSet):
    """API endpoint for the sets (CRUD operations)"""
    serializer_class = WorkingSetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Only allow access to appropriate (owned) object(s)"""
        return WorkingSet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user field to the currently authenticated (and requested) user."""
        serializer.save(user=self.request.user)