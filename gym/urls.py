from django.urls import path
from rest_framework import urlpatterns
from rest_framework.routers import SimpleRouter
from .views import(
    GymViewSet,
    TrainerViewset,
    TraineeViewSet,
    DietAndWorkoutViewSet
)

router = SimpleRouter()

router.register(r'gym', GymViewSet)
router.register(r'trainer', TrainerViewset)
router.register(r'trainee', TraineeViewSet)
router.register(r'dietandworkout', DietAndWorkoutViewSet)

urlpatterns += router.urls


