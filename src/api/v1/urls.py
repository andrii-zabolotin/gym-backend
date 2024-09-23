from django.urls import path, include

from api.auth.auth import CreateTokenView
from api.v1.group_permission.urls import permission_router, group_router

app_name = "api"

urlpatterns = [
    path("token/", CreateTokenView.as_view(), name="token"),
    path("user/", include("api.v1.user.urls")),
    path("", include("api.v1.subscription.urls")),
    path("", include("api.v1.trainings.urls")),
    path("", include("api.v1.attendance.urls")),
    path("", include(group_router.urls)),
    path("", include(permission_router.urls)),
    path("", include("api.v1.group_permission.urls")),
]
