from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models

from comet_auth.models import UserInformation




class DialogueHistory(models.Model):
    user_information = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    date = models.DateTimeField()
    message = models.TextField()
    message_type = models.TextField()
    message_writer = models.TextField()
    more_info = models.TextField(null=True)

    # --> Hides message from chatbox
    hidden = models.BooleanField(default=False)

    # --> True when message_writer == User AND user is waiting for brain response
    loading = models.BooleanField(default=False)

    # --> True when message_writer == User AND brain does not find response
    response_error = models.BooleanField(default=False)



class Action(models.Model):
    name = models.TextField()



class UserAction(models.Model):
    user_information = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    details = models.TextField()


















