from django.urls import path, include

from api.v1.subscription.views import *

app_name = "api_subscription"

urlpatterns = [
    path("create/", CreateSubscriptionView.as_view(), name="subscription-create"),
    path("list/", ListSubscriptionView.as_view(), name="subscription-list"),
    path(
        "api/v1/subscription/<int:pk>/",
        RetrieveUpdateSubscriptionView.as_view(),
        name="subscription-detail",
    ),
]
