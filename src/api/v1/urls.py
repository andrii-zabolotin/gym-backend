from django.http import JsonResponse
from django.urls import path, include

from api.auth.auth import CreateTokenView

app_name = "api"

urlpatterns = [
    path("token/", CreateTokenView.as_view(), name="token"),
    path("user/", include("api.v1.user.urls")),
    path("subscription/", include("api.v1.subscription.urls")),
    path("trainings/", include("api.v1.trainings.urls")),
]
