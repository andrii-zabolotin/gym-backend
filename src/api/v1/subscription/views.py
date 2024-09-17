from rest_framework import generics, authentication

from api.auth.permissions import IsSuperUser, IsSuperUserOrReadOnly
from api.v1.subscription.serializers import SubscriptionSerializer, SubscriptionUpdateSerializer
from apps.subscriptions.models import Subscription


class CreateSubscriptionView(generics.CreateAPIView):
    """Create a new subscription in the system"""

    serializer_class = SubscriptionSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsSuperUser]


class ListSubscriptionView(generics.ListAPIView):
    """Retrieve a list of subscriptions."""
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.all()


class RetrieveUpdateSubscriptionView(generics.RetrieveUpdateAPIView):
    """Manage the subscription."""

    serializer_class = SubscriptionUpdateSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsSuperUserOrReadOnly]

    def get_queryset(self):
        return Subscription.objects.all()
