from django.db import models


class SubscriptionManager(models.Manager):
    def only_active(self):
        return super().get_queryset().filter(is_active=True)

    def all_with_deleted(self):
        return super().get_queryset()

    def only_deleted(self):
        return super().get_queryset().filter(is_active=False)
