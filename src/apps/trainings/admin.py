from django.contrib import admin

from apps.trainings.models import Training, TrainingUser

admin.site.register(Training)
admin.site.register(TrainingUser)
