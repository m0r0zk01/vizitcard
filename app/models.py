from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from scripts.token_generator import generate_token
from datetime import datetime
from vizitcard.settings import STATIC_ROOT


class User(AbstractUser):
    worker = models.OneToOneField('Worker', on_delete=models.CASCADE, null=True, default=None)
    avatar = models.ImageField(default='img/avatars/default_avatar.png', upload_to='img/avatars/')
    biography = models.TextField(null=True)
    location = models.TextField(null=True)


class Card(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    telegram = models.TextField()
    vk = models.TextField()
    whats_app = models.TextField()
    telephone = models.TextField()
    url = models.TextField()


class Organization(models.Model):
    creator = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    activated = models.BooleanField(default=False)

    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True)
    workers = models.ManyToManyField('Worker')


class Worker(models.Model):
    position = models.TextField(default="", editable=False)
    work_card = models.OneToOneField(Card, on_delete=models.SET_NULL, null=True, default=None)
    org = models.ForeignKey(Organization, null=True, default=None, on_delete=models.CASCADE)


class Token(models.Model):
    token = models.CharField(max_length=30, default=generate_token, null=False)
    token_type = models.CharField(max_length=30, default='activation')
    creation_date = models.DateTimeField(default=timezone.now)
    lifetime = models.IntegerField(default=1)
    user = models.ForeignKey(to=User, blank=True, on_delete=models.PROTECT, null=True)


class OrganizationToken(Token):
    org = models.OneToOneField(Organization, on_delete=models.CASCADE)
