from django.http import JsonResponse
from django.urls import path, include

app_name = "api"

urlpatterns = [
    path("user/", include("api.v1.user.urls"))
]
