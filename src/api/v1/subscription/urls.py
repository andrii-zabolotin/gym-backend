from django.urls import path, include

from api.v1.subscription.views import *

app_name = "api_subscription"

urlpatterns = [
    path("subscriptions/", SubscriptionListAPIView.as_view(), name="subscription-list"),
    path("subscriptions/", SubscriptionCreateAPIView.as_view(), name="subscription-create"),
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
