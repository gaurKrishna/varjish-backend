from django.contrib import admin
from .models import (
    Gym,
    Trainer,
    Trainee,
    DietAndWorkout
)

admin.site.register(Gym)
admin.site.register(Trainer)
admin.site.register(Trainee)
admin.site.register(DietAndWorkout)
# Register your models here.
