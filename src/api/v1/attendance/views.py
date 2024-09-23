from django.core.exceptions import ValidationError
from rest_framework import generics, status, authentication, permissions
from rest_framework.response import Response

from api.v1.attendance.filters import AttendanceFilter, AttendanceTrainingFilter
from api.v1.attendance.serializers import AttendanceSerializer, AttendanceTrainingSerializer
from apps.attendance.models import Attendance, AttendanceTraining


class AttendanceListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    filterset_class = AttendanceFilter

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Attendance.objects.none()

        if self.request.user.is_superuser or self.request.user.is_administrator:
            return Attendance.objects.all()

        return Attendance.objects.filter(user_subscription__user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                e.message_dict,
                status=status.HTTP_400_BAD_REQUEST
            )


class AttendanceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AttendanceSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    queryset = Attendance.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_administrator:
            return Attendance.objects.all()

        return Attendance.objects.filter(user_subscription__user=self.request.user)


class AttendanceTrainingListCreateAPIView(generics.ListCreateAPIView):
    queryset = AttendanceTraining.objects.all()
    serializer_class = AttendanceTrainingSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    filterset_class = AttendanceTrainingFilter

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_administrator:
            return AttendanceTraining.objects.all()

        return AttendanceTraining.objects.filter(attendance__user_subscription__user=self.request.user)


class AttendanceTrainingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttendanceTraining.objects.all()
    serializer_class = AttendanceTrainingSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_administrator:
            return AttendanceTraining.objects.all()

        return AttendanceTraining.objects.filter(attendance__user_subscription__user=self.request.user)
