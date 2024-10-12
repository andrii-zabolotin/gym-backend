from django_filters import rest_framework as filters


class AttendanceFilter(filters.FilterSet):
    user_id = filters.NumberFilter(field_name="user_subscription__user__id")
    user_subscription_id = filters.NumberFilter(field_name="user_subscription__id")
