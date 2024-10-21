from rest_framework import serializers

from api.v1.subscription.serializers import UserSubscriptionSerializer, CustomUserSubscriptionSerializer
from api.v1.user.serializers import LimitedUserSerializer
from apps.trainings.models import Training, TrainingUser, TrainingType


class TrainingsSerializer(serializers.ModelSerializer):
    """Serializer for the training object"""

    class Meta:
        model = Training
        fields = "__all__"


class TrainingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingUser
        fields = "__all__"


class TrainingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingType
        fields = "__all__"


class CustomTrainingsSerializer(serializers.ModelSerializer):
    trainer = LimitedUserSerializer(read_only=True)
    training_type = serializers.CharField(source="training_type.name")

    class Meta:
        model = Training
        fields = "__all__"


class CustomTrainingUserSerializer(serializers.ModelSerializer):
    training = CustomTrainingsSerializer(read_only=True)
    user_subscription = CustomUserSubscriptionSerializer(read_only=True)

    class Meta:
        model = TrainingUser
        fields = "__all__"
