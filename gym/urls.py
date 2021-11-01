from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import(
    GymViewSet,
    MyTrainees,
    TrainerByGym,
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
    path("myworkoutplan/", MyDietAndWorkout.as_view(), name="mydietplan"),
    path("trainerbygym/<int:gym>/", TrainerByGym.as_view(), name="trainerbygym"),
    path("mytrainees/", MyTrainees.as_view(), name="mytrainees")
]

urlpatterns += router.urls


