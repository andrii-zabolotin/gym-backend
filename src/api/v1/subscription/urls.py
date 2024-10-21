from django.urls import path, include
from rest_framework import routers

from api.v1.subscription.views import *

app_name = "api_subscription"

router = routers.SimpleRouter()
router.register('subscription-types', SubscriptionTypeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("subscriptions/", SubscriptionListCreateAPIView.as_view(), name="subscription"),
    path("subscriptions-users/", UserSubscriptionListCreateAPIView.as_view(), name="subscription-user-list"),
    path(
        "subscriptions/<int:pk>/",
        SubscriptionRetrieveUpdateAPIView.as_view(),
        name="subscription-detail",
    ),
    path(
        "subscriptions-users/<int:pk>/",
        UserSubscriptionRetrieveUpdateDestroyAPIView.as_view(),
        name="subscription-user-detail",
    ),
]
