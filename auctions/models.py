from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    date = models.DateTimeField()
    image = models.URLField()
    price = models.FloatField()
    category = models.CharField(max_length=30)
    closed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    winner = models.ForeignKey(User, null=True, default=None, on_delete=models.SET_NULL, related_name="winner")


class Bid(models.Model):
    price = models.FloatField()
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.CharField(max_length=400)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)