# Django & DRF
from rest_framework import viewsets, permissions
from rest_framework.response import Response

# App
from fitness.models import MuscleGroup, Exercise, Workout, WorkingSet
from .serializers import MuscleGroupSerializer, ExerciseSerializer, WorkoutSerializer, WorkingSetSerializer
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