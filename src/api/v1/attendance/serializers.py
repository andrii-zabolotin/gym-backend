from rest_framework import serializers

from api.v1.subscription.serializers import SubscriptionUserSerializer
from apps.attendance.models import AttendanceTraining


class AttendanceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_subscription = SubscriptionUserSerializer()
    attendance_time = serializers.DateTimeField()


class AttendanceTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceTraining
        fields = "__all__"
