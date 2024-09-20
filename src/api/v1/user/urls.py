from django.http import JsonResponse
from django.urls import path, include

from api.v1.user.views import CreateUserView, ManageUserView

app_name = "api_user"

urlpatterns = [
    path("", CreateUserView.as_view(), name="user-create"),
    path("me/", ManageUserView.as_view(), name="user-manage"),
]
