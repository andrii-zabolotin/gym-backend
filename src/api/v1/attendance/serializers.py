from rest_framework import serializers

from api.v1.subscription.serializers import CustomUserSubscriptionSerializer
from api.v1.trainings.serializers import CustomTrainingsSerializer
from apps.attendance.models import Attendance


class CreateAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"


class AttendanceSerializer(serializers.ModelSerializer):
    training = CustomTrainingsSerializer(read_only=True)
    user_subscription = CustomUserSubscriptionSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "user_subscription", "attendance_time", "training"]
