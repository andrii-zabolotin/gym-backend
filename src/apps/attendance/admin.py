from django.contrib import admin

from apps.attendance.models import AttendanceTraining, Attendance

admin.site.register(AttendanceTraining)
admin.site.register(Attendance)
