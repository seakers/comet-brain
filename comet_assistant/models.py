from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models

from comet_auth.models import UserInformation




class DialogueHistory(models.Model):
    user_information = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    message = models.TextField()
    message_type = models.TextField()
    writer = models.TextField()
    date = models.DateTimeField()



class Action(models.Model):
    name = models.TextField()



class UserAction(models.Model):
    user_information = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    details = models.TextField()


















