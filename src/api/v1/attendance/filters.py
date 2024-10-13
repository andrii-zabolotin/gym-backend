from django_filters import rest_framework as filters

from apps.trainings.models import TrainingType


class AttendanceFilter(filters.FilterSet):
    user_id = filters.NumberFilter(field_name="user_subscription__user__id")
    user_subscription_id = filters.NumberFilter(field_name="user_subscription__id")
    training_type = filters.ChoiceFilter(field_name="training__training_type", choices=[(type.id, type.name) for type in TrainingType.objects.all()])
    date = filters.DateFilter(field_name="attendance_time__date")
    trainer_id = filters.CharFilter(field_name="training__trainer__id")
