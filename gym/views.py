from django.db.models.base import Model
from django.db.models.query import QuerySet
from rest_framework import response
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
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
    DietAndWorkOutSerializer,
    TrainerDepthSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from authentication.serializers import UserSerializer

class GymViewSet(ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    permission_classes = [IsAuthenticated]
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

class MyDietAndWorkout(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if not request.user.role == "TRAINEE":
            return Response({"status": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

        trainee = Trainee.objects.get(user=request.user)

        diet_workout = DietAndWorkout.objects.get(trainee=trainee)

        response_data = DietAndWorkOutSerializer(diet_workout).data

        response_data["Trainer_name"] = diet_workout.trainer.user.firstname + " " + diet_workout.trainer.user.lastname

        response_data["Gym"] = diet_workout.trainer.gym.name

        return Response(response_data, status=status.HTTP_200_OK)

class TrainerByGym(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        gym_id = kwargs.get("gym", None)

        if gym_id:
            gym = Gym.objects.get(id=gym_id)
            user_trainers = Trainer.objects.filter(gym=gym).values_list("user", flat=True)
            response_data = UserSerializer(user_trainers).data

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Gym id must be paased to get all trainers"}, status=status.HTTP_400_BAD_REQUEST)

class MyTrainees(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        trainer = Trainer.objects.get(user=request.user)
        user = Trainee.objects.filter(trainer = trainer).values_list("user", flat=True)
        response_data = UserSerializer(user, many=True).data

        return Response(response_data, status=status.HTTP_200_OK)  