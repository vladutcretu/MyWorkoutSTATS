# Django & DRF
from rest_framework import viewsets, permissions
from rest_framework.response import Response

# App
from fitness.models import MuscleGroup
from .serializers import MuscleGroupSerializer
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