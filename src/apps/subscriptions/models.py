from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from apps.attendance.models import Attendance


class SubscriptionType(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")

    name = models.CharField(verbose_name=_("Subscription name"))
    subscription_type = models.ForeignKey("SubscriptionType", on_delete=models.PROTECT, verbose_name=_("Subscription type"))
    validity_period = models.IntegerField(verbose_name=_("Validity period"))
    available_number_of_visits = models.IntegerField(verbose_name=_("Available number of visits"))
    price = models.IntegerField(verbose_name=_("Price"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()

    def restore(self):
        self.is_active = True
        self.save()

    def __str__(self):
        return f"{self.name} - {self.price} {self.get_subscription_type_display()}"


class UserSubscription(models.Model):

    purchase_at = models.DateTimeField(auto_now_add=True)
    subscription = models.ForeignKey("subscriptions.Subscription", on_delete=models.PROTECT, verbose_name=_("Subscription"))
    user = models.ForeignKey("user.CustomUser", on_delete=models.PROTECT, verbose_name=_("User"))

    @property
    def expiration_at(self):
        if self.subscription and self.purchase_at:
            return self.purchase_at + timedelta(days=self.subscription.validity_period)
        return None

    @property
    def used_visits(self):
        used_visits = Attendance.objects.filter(user_subscription=self).count()

        return max(used_visits, 0)

    def __str__(self):
        return f"[{self.pk}] {self.user.phone} - {self.subscription.name}"
