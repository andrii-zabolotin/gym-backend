from django_filters import rest_framework as filters

from apps.trainings.models import TrainingType


class TrainingFilter(filters.FilterSet):
    trainer_id = filters.NumberFilter(field_name="trainer__id")
    date = filters.DateFilter(field_name="date")
    type = filters.ChoiceFilter(field_name="training_type", choices=[(type.code, type.name) for type in TrainingType.objects.all()])


class TrainingUserFilter(filters.FilterSet):
    user_subscription_id = filters.NumberFilter(field_name="user_subscription__id")
    training_id = filters.NumberFilter(field_name="training__id")
    user_id = filters.NumberFilter(field_name="user_subscription__user__id")
