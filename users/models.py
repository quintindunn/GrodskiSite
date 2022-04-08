from django.db import models
from django.contrib.auth.models import AbstractUser

from classes.models import Class


class User(AbstractUser):
    classes = models.ManyToManyField(Class)
    grade = models.IntegerField(default=0)
    is_editor = models.BooleanField(default=False)

