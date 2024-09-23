from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.group_permission.views import *

app_name = "api_group_permission"

group_router = DefaultRouter()
group_router.register("groups", viewset=GroupViewSet, basename="group")
permission_router = DefaultRouter()
permission_router.register("permissions", viewset=PermissionViewSet, basename="permission")

urlpatterns = [
    path("groups-users/<int:user_id>/<int:group_id>", UserGroupViewSet.as_view({'delete': 'destroy'})),
    path("groups-users/<int:pk>", UserGroupViewSet.as_view({'get': 'retrieve'})),
    path("groups-users/", UserGroupViewSet.as_view({'get': 'list', 'post': 'create'}))
]
