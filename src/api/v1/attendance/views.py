from django.core.exceptions import ValidationError
from rest_framework import generics, status, authentication, permissions
from rest_framework.response import Response

from api.v1.attendance.filters import AttendanceFilter
from api.v1.attendance.serializers import AttendanceSerializer, CreateAttendanceSerializer
from apps.attendance.models import Attendance


class AttendanceListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    filterset_class = AttendanceFilter

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateAttendanceSerializer

        return AttendanceSerializer


    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Attendance.objects.none()

        if self.request.user.is_superuser or self.request.user.is_administrator:
            return Attendance.objects.all().order_by('-attendance_time')

        return Attendance.objects.filter(user_subscription__user=self.request.user).order_by('-attendance_time')

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                e.message_dict,
                status=status.HTTP_400_BAD_REQUEST
            )


class AttendanceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    queryset = Attendance.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return CreateAttendanceSerializer

        return AttendanceSerializer


    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_administrator:
            return Attendance.objects.all()

        return Attendance.objects.filter(user_subscription__user=self.request.user)
