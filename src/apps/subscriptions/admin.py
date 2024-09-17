from django.contrib import admin

from apps.subscriptions.models import Subscription, UserSubscription

admin.site.register(Subscription)
admin.site.register(UserSubscription)
