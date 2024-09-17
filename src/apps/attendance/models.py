from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.trainings.models import Training
from apps.user.models import CustomUser


class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name=_("User"))
    attendance_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Attendance Datetime"))

    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")

    def __str__(self):
        return f"Attendance of {self.user} on {self.datetime}"


class AttendanceTraining(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.PROTECT, verbose_name=_("Attendance"))
    training = models.ForeignKey(Training, on_delete=models.PROTECT, verbose_name=_("Training"))
    check_in_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Check-in Time"))

    class Meta:
        verbose_name = _("Attendance Training")
        verbose_name_plural = _("Attendance Trainings")
        unique_together = ('attendance', 'training')

    def __str__(self):
        return f"Training {self.training.training_type} for {self.attendance.user} on {self.attendance.attendance_time}"