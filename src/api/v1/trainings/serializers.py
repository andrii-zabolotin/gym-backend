from rest_framework import serializers

from apps.trainings.models import Training, TrainingUser


class TrainingsSerializer(serializers.ModelSerializer):
    """Serializer for the training object"""

    class Meta:
        model = Training
        fields = "__all__"


class TrainingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingUser
        fields = "__all__"
