from django.urls import path

from api.v1.attendance.views import *

app_name = "api_attendance"

urlpatterns = [
    path("attendances/", AttendanceListCreateAPIView.as_view(), name="attendance"),
    path("attendances/<int:pk>/", AttendanceRetrieveUpdateDestroyAPIView.as_view(), name="attendance-detail"),
]
