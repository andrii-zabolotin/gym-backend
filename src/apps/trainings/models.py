from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.user.models import CustomUser


class Training(models.Model):
    TRAINING_TYPES = (
        ('personal', 'Personal Training'),
        ('yoga', 'Yoga'),
        ('massage', 'Massage'),
        ('stretching', 'Stretching'),
        ('trx', 'TRX'),
    )

    description = models.CharField(max_length=255, verbose_name=_("Description"), null=True, blank=True)
    training_type = models.CharField(max_length=15, choices=TRAINING_TYPES, verbose_name=_("Training type"))
    trainer = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name=_("Trainer"),
                                limit_choices_to={'is_trainer': True})
    date = models.DateField(verbose_name=_("Date"))
    start_time = models.TimeField(verbose_name=_("Start time"))
    end_time = models.TimeField(verbose_name=_("End time"))
    max_participants = models.PositiveIntegerField(default=1, verbose_name=_("Maximum number of participants"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.training_type} - {self.date} ({self.start_time} - {self.end_time})"


class TrainingUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name=_("Participant"))
    training = models.ForeignKey(Training, on_delete=models.PROTECT, verbose_name=_("Training"))
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Registration date"))

    class Meta:
        unique_together = ('user', 'training')

    def __str__(self):
        return f"{self.user.email} - {self.training.training_type} ({self.training.date})"
