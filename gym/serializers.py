from django.db import models
from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from rest_framework.utils import field_mapping, model_meta
from .models import (
    Gym,
    Trainer,
    Trainee,
    DietAndWorkout
)


class GymSerializer(ModelSerializer):
    class Meta:
        model = Gym
        fields = "__all__"

class TrainerSerializer(ModelSerializer):
    class Meta:
        model = Trainer
        fields = "__all__"

class TraineeSieralizer(ModelSerializer):
    class Meta:
        model = Trainee
        fields = "__all__"

class DietAndWorkOutSerializer(ModelSerializer):
    class Meta:
        model = DietAndWorkout
        fields = "__all__"