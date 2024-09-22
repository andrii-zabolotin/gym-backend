from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from apps.subscriptions.models import UserSubscription
from apps.trainings.models import Training


class Attendance(models.Model):
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.PROTECT, verbose_name=_("User"))
    attendance_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Attendance Datetime"))

    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")

    def clean(self):
        super().clean()

        # Check attendance limit
        if self.user_subscription.subscription.available_number_of_visits <= Attendance.objects.filter(
                user_subscription=self.user_subscription).count():
            raise ValidationError(
                {
                    "user_subscription": f"Max visits limit reached ({self.user_subscription.subscription.available_number_of_visits})."
                }
            )

        # Check expiration date
        if self.user_subscription.expiration_at < timezone.now():
            raise ValidationError(
                {
                    "user_subscription": f"Subscription expired at {self.user_subscription.expiration_at}"
                }
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Attendance of {self.user_subscription.user.phone} on {self.attendance_time}"


class AttendanceTraining(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.PROTECT, verbose_name=_("Attendance"))
    training = models.ForeignKey(Training, on_delete=models.PROTECT, verbose_name=_("Training"))

    class Meta:
        verbose_name = _("Attendance Training")
        verbose_name_plural = _("Attendance Trainings")
        unique_together = ('attendance', 'training')

    def __str__(self):
        return f"Training {self.training.training_type} for {self.attendance.user_subscription.user.phone} on {self.check_in_time}"
