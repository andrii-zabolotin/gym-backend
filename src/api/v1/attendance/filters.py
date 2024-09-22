from django_filters import rest_framework as filters


class AttendanceFilter(filters.FilterSet):
    user_id = filters.NumberFilter(field_name="user_subscription__user__id")
    user_subscription_id = filters.NumberFilter(field_name="user_subscription__id")


class AttendanceTrainingFilter(filters.FilterSet):
    user_id = filters.NumberFilter(field_name="attendance__user_subscription__user__id")
    user_subscription_id = filters.NumberFilter(field_name="attendance__user_subscription__id")
    training = filters.NumberFilter(field_name="training__id")
    attendance = filters.NumberFilter(field_name="attendance__id")
