from django.db.models.base import Model
from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from .models import (
    Gym,
    Trainee,
    Trainer,
    DietAndWorkout
)
from .serializers import(
    GymSerializer,
    TrainerSerializer,
    TraineeSieralizer,
    DietAndWorkOutSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny


class GymViewSet(ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post']

class TrainerViewset(ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

class TraineeViewSet(ModelViewSet):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSieralizer
    permission_classes = [IsAuthenticated]
    http_method_name = ['get', 'post']

class DietAndWorkoutViewSet(ModelViewSet):
    queryset = DietAndWorkout.objects.all()
    serializer_class = DietAndWorkOutSerializer
    permissions_classes = [IsAuthenticated]
    http_method_name = ['get', 'post']