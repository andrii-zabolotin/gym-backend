from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.subscriptions.models import UserSubscription
from apps.user.models import CustomUser

TRAINING_TYPES = (
    ("personal", "Personal Training"),
    ("yoga", "Yoga"),
    ("massage", "Massage"),
    ("stretching", "Stretching"),
    ("trx", "TRX"),
)


class Training(models.Model):
    description = models.CharField(max_length=255, verbose_name=_("Description"), null=True, blank=True)
    training_type = models.CharField(max_length=15, choices=TRAINING_TYPES, verbose_name=_("Training type"))
    trainer = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name=_("Trainer"),
                                limit_choices_to={"is_staff": True})
    date = models.DateField(verbose_name=_("Date"))
    start_time = models.TimeField(verbose_name=_("Start time"))
    end_time = models.TimeField(verbose_name=_("End time"))
    max_participants = models.PositiveIntegerField(default=1, verbose_name=_("Maximum number of participants"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.pk:
            participants_count = TrainingUser.objects.filter(training=self).count()
            if self.max_participants is not None and participants_count > self.max_participants:
                raise ValidationError({
                    "max_participants": f"Max participants ({self.max_participants}) cannot be less than current participants ({participants_count})."
                })

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_training_type_display()} - {self.date} ({self.start_time} - {self.end_time})"


class TrainingUser(models.Model):
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.PROTECT, verbose_name=_("Participant"))
    training = models.ForeignKey(Training, on_delete=models.PROTECT, verbose_name=_("Training"))
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Registration date"))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user_subscription", "training"], name="unique_training_user")
        ]

    def clean(self):
        super().clean()
        participants_count = TrainingUser.objects.filter(training=self.training).count()
        if participants_count >= self.training.max_participants:
            raise ValidationError({
                "training": f"The maximum number of participants ({self.training.max_participants}) has already been reached."
            })

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_subscription.user.pk} - {self.training.training_type} ({self.training.date})"
