# Django & DRF
from rest_framework import generics, permissions, throttling, status
from rest_framework.response import Response

# App
from core.models import CustomUser
from core.api.serializers import SignUpSerializer


class SignUpAPIView(generics.CreateAPIView):
    """API endpoint for sign up"""
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttling.AnonRateThrottle]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'message': 'User account (via API endpoint) successfully created',
                'username': user.username,
                'email': user.email
            },
            status=status.HTTP_201_CREATED
        )