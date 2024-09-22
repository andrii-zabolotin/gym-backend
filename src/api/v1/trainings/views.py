from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from rest_framework import generics, authentication, permissions, status
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from api.v1.trainings.filters import TrainingFilter, TrainingUserFilter
from api.v1.trainings.serializers import TrainingsSerializer, TrainingUserSerializer
from apps.trainings.models import Training, TrainingUser


class TrainingListCreateAPIView(generics.ListCreateAPIView):
    """Create a new subscription in the system"""

    serializer_class = TrainingsSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = []
    filterset_class = TrainingFilter

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.DjangoModelPermissions]

        return super().get_permissions()

    def get_queryset(self):
        if not self.request.user.is_anonymous and (self.request.user.is_superuser or self.request.user.is_administrator):
            return Training.objects.all()

        return Training.objects.filter(date__gte=timezone.now().date())


class TrainingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TrainingsSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = []

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = [permissions.DjangoModelPermissions]

        return super().get_permissions()

    def get_queryset(self):
        if not self.request.user.is_anonymous and (self.request.user.is_superuser or self.request.user.is_administrator):
            return Training.objects.all()

        return Training.objects.filter(date__gte=timezone.now().date())

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                e.message_dict,
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        """Destroy a model instance."""
        try:
            return super().destroy(request, *args, **kwargs)
        except IntegrityError as e:
            # Handle IntegrityError when object is protected
            return Response(
                {"error": "The object cannot be deleted. It is used in other entries."},
                status=status.HTTP_400_BAD_REQUEST
            )


class TrainingUserListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TrainingUserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    filterset_class = TrainingUserFilter

    def get_queryset(self):
        if not self.request.user.is_anonymous and (self.request.user.is_superuser or self.request.user.is_administrator):
            return TrainingUser.objects.all()

        return TrainingUser.objects.filter(user_subscription__user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                e.message_dict,
                status=status.HTTP_400_BAD_REQUEST
            )


class TrainingUserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TrainingUserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        if not self.request.user.is_anonymous and (self.request.user.is_superuser or self.request.user.is_administrator):
            return TrainingUser.objects.all()

        return TrainingUser.objects.filter(user_subscription__user=self.request.user)
