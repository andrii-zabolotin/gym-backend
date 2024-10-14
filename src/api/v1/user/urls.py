from django.urls import path

from api.v1.user.views import CreateUserView, ManageUserView, UserStaffListAPIView, UserRetrieveUpdateAPIView, \
    UserGetAPIView

app_name = "api_user"

urlpatterns = [
    path("", CreateUserView.as_view(), name="user-create"),
    path("<int:pk>/", UserRetrieveUpdateAPIView.as_view(), name="user-retrieve"),
    path("staff/", UserStaffListAPIView.as_view(), name="user-staff"),
    path("list/", UserGetAPIView.as_view(), name="user-list"),
    path("me/", ManageUserView.as_view(), name="user-manage"),
]
