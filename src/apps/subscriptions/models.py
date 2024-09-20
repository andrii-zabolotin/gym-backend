from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

from apps.subscriptions.managers import SubscriptionManager
from apps.user.models import CustomUser


class Subscription(models.Model):
    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")

    SUBSCRIPTION_TYPES = (
        ('general', 'General'),
        ('group', 'Group Classes'),
        ('personal', 'Personal Training'),
        ('massage', 'Massage'),
    )

    name = models.CharField(verbose_name=_("Subscription name"))
    subscription_type = models.CharField(max_length=15, choices=SUBSCRIPTION_TYPES, verbose_name=_("Subscription type"))
    validity_period = models.IntegerField(verbose_name=_("Validity period"))
    available_number_of_visits = models.IntegerField(verbose_name=_("Available number of visits"))
    price = models.IntegerField(verbose_name=_("Price"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = SubscriptionManager()

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
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT, verbose_name=_("Subscription"))
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name=_("User"))

    @property
    def expiration_at(self):
        if self.subscription and self.purchase_at:
            return self.purchase_at + timedelta(days=self.subscription.validity_period)
        return None

    def __str__(self):
        return f"{self.user.phone} - {self.subscription.name}"
