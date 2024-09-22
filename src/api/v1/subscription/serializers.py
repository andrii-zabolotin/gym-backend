from rest_framework import serializers

from apps.subscriptions.models import Subscription, UserSubscription


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for the subscription object"""

    class Meta:
        model = Subscription
        fields = (
            "pk",
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
