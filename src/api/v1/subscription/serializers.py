from rest_framework import serializers

from api.v1.user.serializers import LimitedUserSerializer
from apps.subscriptions.models import Subscription, UserSubscription, SubscriptionType


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for the subscription object"""
    class Meta:
        model = Subscription
        fields = (
            "id",
            "name",
            "subscription_type",
            "validity_period",
            "available_number_of_visits", "price"
        )


class CustomSubscriptionSerializer(serializers.ModelSerializer):
    subscription_type = serializers.CharField(source="subscription_type.name")

    class Meta:
        model = Subscription
        fields = (
            "id",
            "name",
            "subscription_type",
            "validity_period",
            "available_number_of_visits", "price"
        )


class SubscriptionUpdateSerializer(serializers.ModelSerializer):
    """Serializer for the subscription object"""

    class Meta:
        model = Subscription
        fields = "__all__"


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = "__all__"


class CustomUserSubscriptionSerializer(serializers.ModelSerializer):
    user = LimitedUserSerializer(read_only=True)
    subscription = CustomSubscriptionSerializer(read_only=True)
    expiration_at = serializers.SerializerMethodField()
    used_visits = serializers.SerializerMethodField()

    class Meta:
        model = UserSubscription
        fields = ["id", "purchase_at", "subscription", "user", "expiration_at", "used_visits"]

    def get_expiration_at(self, obj):
        return obj.expiration_at

    def get_used_visits(self, obj):
        return obj.used_visits


class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = "__all__"
