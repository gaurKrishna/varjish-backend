from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import(
    GymViewSet,
    TrainerViewset,
    TraineeViewSet,
    DietAndWorkoutViewSet,
    MyDietAndWorkout
)

router = SimpleRouter()

router.register(r'gym', GymViewSet)
router.register(r'trainer', TrainerViewset)
router.register(r'trainee', TraineeViewSet)
router.register(r'dietandworkout', DietAndWorkoutViewSet)

urlpatterns = [
    path("myworkoutplan/", MyDietAndWorkout.as_view(), name="mydietplan")
]

urlpatterns += router.urls


