from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from scripts.token_generator import generate_token
from datetime import datetime


class User(AbstractUser):
    pass


class Card(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    telegram = models.TextField()
    vk = models.TextField()
    whats_app = models.TextField()
    telephone = models.TextField()
    url = models.TextField()


class Worker(User):
    position = models.TextField()
    photo = models.ImageField()
    work_card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True)


class Organization(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()

    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True)

    workers = models.ManyToManyField


class Token(models.Model):
    token = models.CharField(max_length=30, default=generate_token(), null=False)
    user = models.ForeignKey(to=User, blank=True, on_delete=models.PROTECT, null=True)
    creation_date = models.DateTimeField(default=timezone.now())
