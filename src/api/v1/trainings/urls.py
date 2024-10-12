from django.urls import path, include
from rest_framework import routers

from api.v1.trainings.views import *

app_name = "api_trainings"

router = routers.SimpleRouter()
router.register('training-types', TrainingTypeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("trainings/", TrainingListCreateAPIView.as_view(), name="training"),
    path("trainings/<int:pk>/", TrainingRetrieveUpdateDestroyAPIView.as_view(), name="training-detail"),
    path("trainings-users/<int:pk>/", TrainingUserRetrieveUpdateDestroyAPIView.as_view(), name="training-user-detail"),
    path("trainings-users/", TrainingUserListCreateAPIView.as_view(), name="training-user")
]
