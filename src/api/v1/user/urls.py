from django.http import JsonResponse
from django.urls import path, include

from api.v1.user.views import CreateUserView, ManageUserView, UserListAPIView

app_name = "api_user"

urlpatterns = [
    path("", CreateUserView.as_view(), name="user-create"),
    path("list/", UserListAPIView.as_view(), name="user-list"),
    path("me/", ManageUserView.as_view(), name="user-manage"),
]
