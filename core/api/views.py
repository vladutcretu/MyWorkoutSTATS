# Django & DRF
from rest_framework import generics, permissions, throttling, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


# App
from core.api.serializers import (
    SignUpSerializer,
    LogInSerializer,
    CustomUserSerializer,
)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class SignUpAPIView(generics.CreateAPIView):
    """
    API endpoint for sign up
    """

    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttling.AnonRateThrottle]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response(
            {
                "message": "User account (via API) successfully created",
                "username": user.username,
                "email": user.email,
                "refresh token": tokens["refresh"],
                "access token": tokens["access"],
            },
            status=status.HTTP_201_CREATED,
        )


class LogInAPIView(APIView):
    """
    API endpoint for log in
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            tokens = get_tokens_for_user(user)
            return Response(
                {
                    "message": "Successfully logged in (via API).",
                    "username": user.username,
                    "refresh token": tokens["refresh"],
                    "access token": tokens["access"],
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for the user profile
    """

    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Only allow access to appropriate (owned) object(s)"""
        return self.request.user

    def update(self, request, *args, **kwargs):
        """Overwrite update method to display a personalized message"""
        response = super().update(request, *args, **kwargs)
        return Response(
            {
                "message": "Profile updated successfully (via API endpoint).",
                "data": response.data,
            },
            status=status.HTTP_200_OK,
        )
