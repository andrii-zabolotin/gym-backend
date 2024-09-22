from django.urls import path

from api.v1.trainings.views import *

app_name = "api_trainings"

urlpatterns = [
    path("trainings/", TrainingListCreateAPIView.as_view(), name="training"),
    path("trainings/<int:pk>/", TrainingRetrieveUpdateDestroyAPIView.as_view(), name="training-detail"),
    path("trainings-users/<int:pk>/", TrainingUserRetrieveUpdateDestroyAPIView.as_view(), name="training-user-detail"),
    path("trainings-users/", TrainingUserListCreateAPIView.as_view(), name="training-user")
]
