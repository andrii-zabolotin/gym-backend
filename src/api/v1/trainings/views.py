from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import generics, authentication, permissions, status
from rest_framework.response import Response

from api.v1.trainings.serializers import TrainingsSerializer, TrainingUserSerializer
from apps.trainings.models import Training, TrainingUser


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                "trainer_id",
                OpenApiTypes.NUMBER,
                description="Trainer id",
            ),
            OpenApiParameter(
                "type",
                OpenApiTypes.STR,
                description="Type of training",
                enum=["stretching", "trx", "massage", "yoga", "personal"],
            ),
            OpenApiParameter(
                "date",
                OpenApiTypes.DATE,
                description="Training date [YYYY-MM-DD]",
            ),
        ]
    )
)
class TrainingListCreateAPIView(generics.ListCreateAPIView):
    """Create a new subscription in the system"""

    serializer_class = TrainingsSerializer
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.DjangoModelPermissions]

    def get_queryset(self):
        date = self.request.GET.get("date", None)
        trainer = self.request.GET.get("trainer_id", None)
        training_type = self.request.GET.get("type", None)
        params = {}

        if date:
            try:
                datetime.fromisoformat(date)
            except ValueError:
                return Response(
                    {"error": "Incorrect data format, should be YYYY-MM-DD."},
                    status.HTTP_400_BAD_REQUEST
                )
            if datetime.strptime(date, "%Y-%m-%d").date() < datetime.now().date():
                return Response(
                    {"error": "Date shouldn't be less than today."}, status=status.HTTP_400_BAD_REQUEST
                )
            params["date"] = date

        if trainer:
            for char in trainer:
                if ord(char) < 48 or ord(char) > 57:
                    return Response(
                        {"error": "Incorrect trainer id format, should be integer."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            params["trainer"] = trainer

        if training_type:
            if training_type not in ["stretching", "trx", "massage", "yoga", "personal"]:
                return Response(
                    {"error": "Incorrect training type format, should be ['stretching', 'trx', 'massage', 'yoga', 'personal']."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            params["training_type"] = training_type

        today = timezone.now().date()
        if date:
            return Training.objects.filter(date__gte=today, **params)
        else:
            return Training.objects.filter(**params)


class TrainingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Training.objects.all()
    serializer_class = TrainingsSerializer
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]
    # permission_classes = [permissions.DjangoModelPermissions]

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return response
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


class TrainingUserAPIView(generics.ListCreateAPIView):
    serializer_class = TrainingUserSerializer
    queryset = TrainingUser.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return response
        except ValidationError as e:
            return Response(
                e.message_dict,
                status=status.HTTP_400_BAD_REQUEST
            )
