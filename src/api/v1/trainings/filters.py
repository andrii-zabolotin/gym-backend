from django.utils import timezone
from django.db import models
from django_filters import rest_framework as filters

from apps.trainings.models import TrainingType


class TrainingFilter(filters.FilterSet):
    training_id = filters.NumberFilter(field_name="id")
    trainer_id = filters.NumberFilter(field_name="trainer__id")
    date = filters.DateFilter(field_name="date")
    training_type = filters.ChoiceFilter(field_name="training_type", choices=[(type.id, type.name) for type in TrainingType.objects.all()])
    relevance = filters.ChoiceFilter(choices=[(1, "Past"), (2, "Future")], method='filter_relevance')

    def filter_relevance(self, queryset, name, value):
        now = timezone.now()
        if value == '1':  # Past
            return queryset.filter(end_time__lt=now.time(), date__lte=now.date()) | queryset.filter(date__lte=now.date())
        elif value == '2':  # Future
            return queryset.filter(date__gt=now.date()) | queryset.filter(date=now.date(), start_time__gt=now.time())
        return queryset


class TrainingUserFilter(filters.FilterSet):
    user_subscription_id = filters.NumberFilter(field_name="user_subscription__id")
    training_id = filters.NumberFilter(field_name="training__id")
    user_id = filters.NumberFilter(field_name="user_subscription__user__id")
