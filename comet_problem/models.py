from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models

from comet_auth.models import UserInformation




class Problem(models.Model):
    name = models.TextField()



class UserProblem(models.Model):
    user_information = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)



class Architecture(models.Model):
    user_information = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    representation = models.TextField()
    evaluation_status = models.BooleanField(default=False)



class Objective(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    name = models.TextField()
    type = models.TextField()



class ObjectiveValue(models.Model):
    architecture = models.ForeignKey(Architecture, on_delete=models.CASCADE)
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    value = models.FloatField()
    explanation = models.TextField()



class Parameter(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    name = models.TextField()
    units = models.TextField()
    type = models.TextField()  # item | list
    value = models.TextField()


class Decision(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    name = models.TextField()
    type = models.TextField()  # down-selecting | standard-form


class Alternative(models.Model):
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE)
    value = models.TextField()
    description = models.TextField()
