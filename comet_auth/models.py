from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models

from rest_framework import serializers



class UserInformation(models.Model):

    # Primary key tuple
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    # Websockets communication
    channel_name = models.CharField(max_length=120)

    class Meta:
        unique_together = ("session", "user")