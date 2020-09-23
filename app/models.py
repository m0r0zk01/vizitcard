from django.db import models
from django.contrib.auth.models import AbstractUser


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
