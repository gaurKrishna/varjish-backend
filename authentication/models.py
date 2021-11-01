from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, email, role, password, firstname = None, lastname = None, contact_number = None, profile = None):
        if email is None:
            raise TypeError("Email address is required to create user")

        user = self.model(
            email = self.normalize_email(email), 
            role = role,
            firstname = firstname, 
            lastname = lastname, 
            contact_number = contact_number,
            profile = profile
        )

        print(profile)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if email is None:
            raise TypeError("Email address is required to create super user")

        user = self.create_user(email, "ADMIN", password)
        user.is_staff = True
        user.is_superuser = True 
        user.save(using=self._db)
        return user

ROLES = [
    ("TRAINEE", "TRAINEE"),
    ("TRAINER", "TRAINER"),
    ("GYM_ADMIN", "GYM_ADMIN"),
    ("ADMIN", "ADMIN")
]

class User(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(max_length=255, null=True)
    lastname = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, db_index=True, unique=True)
    contact_number = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=25, choices=ROLES)
    profile = models.ImageField(upload_to = 'files/', null=True)

    class Meta:
        app_label = "authentication"

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email