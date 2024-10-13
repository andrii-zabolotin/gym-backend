from django.contrib.auth import get_user_model
from rest_framework import generics, authentication, permissions

from api.v1.user.filters import UserFilter
from api.v1.user.serializers import UserSerializer, LimitedUserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    permission_classes = []

    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class UserListAPIView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = LimitedUserSerializer
    authentication_classes = []
    permission_classes = []
    filterset_class = UserFilter
