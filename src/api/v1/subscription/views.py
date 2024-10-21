from rest_framework import generics, authentication, status, permissions, viewsets
from rest_framework.permissions import SAFE_METHODS

from api.auth.permissions import IsSuperUser
from api.v1.subscription.filters import SubscriptionFilter, SubscriptionUserFilter
from api.v1.subscription.serializers import SubscriptionSerializer, SubscriptionUpdateSerializer, \
    UserSubscriptionSerializer, CustomUserSubscriptionSerializer, SubscriptionTypeSerializer, \
    CustomSubscriptionSerializer
from apps.subscriptions.models import Subscription, UserSubscription, SubscriptionType


class SubscriptionListCreateAPIView(generics.ListCreateAPIView):
    """Retrieve a list of subscriptions."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = []
    filterset_class = SubscriptionFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CustomSubscriptionSerializer
        return SubscriptionSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.DjangoModelPermissions]

        return super().get_permissions()

    def get_queryset(self):
        if not self.request.user.is_anonymous and (self.request.user.is_superuser or self.request.user.is_administrator):
            return Subscription.objects.all()

        return Subscription.objects.filter(is_active=True)


class SubscriptionRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Manage the subscription."""

    serializer_class = SubscriptionUpdateSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.DjangoModelPermissions]

    def get_queryset(self):
        if not self.request.user.is_anonymous and (self.request.user.is_superuser or self.request.user.is_administrator):
            return Subscription.objects.all()

        return Subscription.objects.filter(is_active=True)


class UserSubscriptionListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    filterset_class = SubscriptionUserFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CustomUserSubscriptionSerializer
        return UserSubscriptionSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return UserSubscription.objects.none()

        if self.request.user.is_superuser or self.request.user.is_administrator:
            return UserSubscription.objects.all().order_by("-purchase_at")

        return UserSubscription.objects.filter(user=self.request.user).order_by("-purchase_at")


class UserSubscriptionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSubscriptionSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_administrator:
            return UserSubscription.objects.all()

        return UserSubscription.objects.filter(user=self.request.user)


class SubscriptionTypeViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeSerializer
    authentication_classes = [authentication.TokenAuthentication]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = []
        else:
            self.permission_classes = [IsSuperUser]

        return super().get_permissions()
