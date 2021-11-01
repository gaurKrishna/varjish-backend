from django.db.models.base import Model
from django.db.models.query import QuerySet
from rest_framework import response
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser

from authentication.models import User
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        response_data = self.get_serializer(instance).data
        user_data = UserSerializer(instance.user, context={"request": request}).data
        response_data = {**response_data, **user_data}
        return Response(response_data, status=status.HTTP_200_OK)

class TraineeViewSet(ModelViewSet):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSieralizer
    permission_classes = [IsAuthenticated]
    http_method_name = ['get', 'post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data["user"] = request.user

        gym = data["gym"]
        trainer = data["trainer"]
        user = request.user

        try:
            trainee = Trainee.objects.get(gym=gym, user=user, trainer=trainer)
            return Response({"error": "Trainee already exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Trainer.DoesNotExist:    
            trainee = Trainee(**data)
            trainee.save()
            trainee_data = TraineeSieralizer(trainee).data 
            return Response(trainee_data, status=status.HTTP_200_OK)
        

class DietAndWorkoutViewSet(ModelViewSet):
    queryset = DietAndWorkout.objects.all()
    serializer_class = DietAndWorkOutSerializer
    permissions_classes = [IsAuthenticated]
    http_method_name = ['get', 'post']
    parser_classes = (MultiPartParser, )

class MyDietAndWorkout(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if not request.user.role == "TRAINEE":
            return Response({"status": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

        trainee = Trainee.objects.get(user=request.user)

        diet_workout = DietAndWorkout.objects.filter(trainee=trainee)

        if len(diet_workout) != 0:
            diet_workout = diet_workout[0]
            response_data = DietAndWorkOutSerializer(diet_workout, context={"request": request}).data
        else:
            response_data = []

        if len(response_data) != 0:
            response_data["Trainer_name"] = diet_workout.trainer.user.firstname + " " + diet_workout.trainer.user.lastname
            response_data["Gym"] = diet_workout.trainer.gym.name

        return Response(response_data, status=status.HTTP_200_OK)

class TrainerByGym(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        gym_id = kwargs.get("gym", None)

        if gym_id:
            gym = Gym.objects.get(id=gym_id)
            trainers = Trainer.objects.filter(gym=gym)
            response_data = []
            for trainer in trainers:
                user_data = UserSerializer(trainer.user, context={"request": request}).data
                user_data["trainer"] = trainer.id
                response_data.append(user_data)

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Gym id must be paased to get all trainers"}, status=status.HTTP_400_BAD_REQUEST)

class MyTrainees(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        trainer = Trainer.objects.get(user=request.user)
        trainees = Trainee.objects.filter(trainer = trainer)

        response_data = []
        for trainee in trainees:
            user_data = UserSerializer(trainee.user, context={"request": request}).data
            user_data["trainee"] = trainee.id
            user_data["trainer"] = trainer.id
            response_data.append(user_data)

        return Response(response_data, status=status.HTTP_200_OK)  