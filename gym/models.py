from django.db import models
from authentication.models import User

class Gym(models.Model):
    name = models.CharField(max_length=255, null=False)
    address = models.TextField(max_length=255, null=False)
    contact_number = models.IntegerField(null=False)

class Trainer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trainer_user")
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name="gym_trainer")


class Trainee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_trainee")
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="trainee_trainer")
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name="gym_trainee")

class DietAndWorkout(models.Model):
    diet_plan = models.FileField(upload_to="files/diet_plan", null=False)
    workout_plan = models.FileField(upload_to="files/workout_plan", null=False)
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name="paln_trainee")
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="plan_trainer")