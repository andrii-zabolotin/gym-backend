from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import generics, authentication, status
from rest_framework.response import Response

from api.auth.permissions import IsSuperUser, IsSuperUserOrReadOnly
from api.v1.subscription.serializers import SubscriptionSerializer, SubscriptionUpdateSerializer
from apps.subscriptions.models import Subscription


class CreateSubscriptionView(generics.CreateAPIView):
    """Create a new subscription in the system"""

    serializer_class = SubscriptionSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsSuperUser]


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                "type",
                OpenApiTypes.STR,
                enum=["all", "deleted"],
            ),
        ]
    )
)
class ListSubscriptionView(generics.ListAPIView):
    """Retrieve a list of subscriptions."""
    serializer_class = SubscriptionSerializer

    def get(self, request, *args, **kwargs):
        type = self.request.query_params.get("type", None)
        user = self.request.user

        if type:
            if type not in ['all', 'deleted']:
                return Response({
                    "detail": "Invalid type parameter. Must be 'all' or 'deleted'."
                },
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif user.is_active is not True and user.is_superuser is not True:
                return Response({
                    "detail": "You do not have permission to perform this action."
                },
                    status=status.HTTP_403_FORBIDDEN
                )

    def get_queryset(self):
        type = self.request.query_params.get("type", None)

        if type:
            if type == "all":
                return Subscription.objects.all()
            elif type == "deleted":
                return Subscription.objects.only_deleted()
        else:
            return Subscription.objects.only_active()


class RetrieveUpdateSubscriptionView(generics.RetrieveUpdateAPIView):
    """Manage the subscription."""

    serializer_class = SubscriptionUpdateSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsSuperUserOrReadOnly]

    def get_queryset(self):
        return Subscription.objects.all()

