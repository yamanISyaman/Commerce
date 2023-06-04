from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class auction(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()

