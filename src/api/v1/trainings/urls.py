from django.urls import path

from api.v1.trainings.views import *

app_name = "api_trainings"

urlpatterns = [
    path("", TrainingListCreateAPIView.as_view(), name="training"),
    path("<int:pk>/", TrainingRetrieveUpdateDestroyAPIView.as_view(), name="training-detail"),
    path("user/", TrainingUserAPIView.as_view(), name="training-user")
]
