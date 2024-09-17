from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.subscriptions.models import UserSubscription
from apps.trainings.models import Training


class Attendance(models.Model):
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.PROTECT, verbose_name=_("User"))
    attendance_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Attendance Datetime"))

    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")

    def __str__(self):
        return f"Attendance of {self.user_subscription.user.email} on {self.datetime}"


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