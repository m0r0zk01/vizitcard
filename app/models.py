from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from scripts.token_generator import generate_token
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import datetime
import os


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
    url = models.CharField(max_length=30, unique=True)
    serialized_array = models.TextField(default='[]')
    image = models.FileField(upload_to='img/cards/cards/')


def upload_path_handler(instance, filename):
    return f'img/cards/{instance.card.id}/{filename}'


class CardFile(models.Model):
    name = models.CharField(max_length=100, default='filename')
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    file = models.FileField(null=True, blank=True, upload_to=upload_path_handler)


_UNSAVED_FILEFIELD = 'unsaved_filefield'


@receiver(pre_save, sender=CardFile)
def skip_saving_file(sender, instance, **kwargs):
    if not instance.pk and not hasattr(instance, _UNSAVED_FILEFIELD):
        setattr(instance, _UNSAVED_FILEFIELD, instance.file)
        instance.file = None


@receiver(post_save, sender=CardFile)
def save_file(sender, instance, created, **kwargs):
    if created and hasattr(instance, _UNSAVED_FILEFIELD):
        instance.file = getattr(instance, _UNSAVED_FILEFIELD)
        instance.save()


class Organization(models.Model):
    creator = models.OneToOneField(User, null=True, on_delete=models.PROTECT)
    name = models.TextField()
    description = models.TextField()
    activated = models.BooleanField(default=False)

    card = models.OneToOneField(Card, null=True, on_delete=models.SET_NULL)


class Worker(models.Model):
    position = models.TextField(default="", editable=False)
    work_card = models.OneToOneField(Card, null=True, default=None, on_delete=models.SET_NULL)
    org = models.ForeignKey(Organization, null=True, default=None, on_delete=models.SET_NULL)


class Token(models.Model):
    token = models.CharField(max_length=30, default=generate_token, null=False)
    token_type = models.CharField(max_length=30, default='activation')
    creation_date = models.DateTimeField(default=timezone.now)
    lifetime = models.IntegerField(default=1)
    user = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.PROTECT)


class OrganizationToken(Token):
    org = models.OneToOneField(Organization, on_delete=models.CASCADE)
