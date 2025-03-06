# Django & DRF
from rest_framework import generics, permissions, throttling, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

# App
from core.api.serializers import (
    SignUpSerializer,
    LogInSerializer,
    CustomUserSerializer,
)


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
        return Response(
            {
                "message": "User account (via API) successfully created",
                "username": user.username,
                "email": user.email,
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
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "message": "Successfully logged in (via API).",
                    "username": user.username,
                    "token": token.key,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogOutAPIView(APIView):
    """
    API endpoint for log out
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {"message": "Successfully logged out (via API)."},
            status=status.HTTP_200_OK,
        )


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
