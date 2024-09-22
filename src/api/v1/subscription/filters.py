from django_filters import rest_framework as filters


class SubscriptionFilter(filters.FilterSet):
    is_active = filters.BooleanFilter(field_name="is_active")


class SubscriptionUserFilter(filters.FilterSet):
    user_id = filters.NumberFilter(field_name="user__id")
    subscription_id = filters.NumberFilter(field_name="subscription__id")
