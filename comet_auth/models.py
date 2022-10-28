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

    # Problem Info
    problem_id = models.IntegerField(default=1)

    class Meta:
        unique_together = ("session", "user")


    ########################
    ### AWS 2.0 Backends ###
    ########################

    # --> Locks
    service_lock = models.BooleanField(default=False)
    design_evaluator_service_lock = models.BooleanField(default=False)
    genetic_algorithm_service_lock = models.BooleanField(default=False)

    # --> Design Evaluator
    design_evaluator_instance_count = models.IntegerField(default=3)
    design_evaluator_request_queue_name = models.TextField(null=True)  # user-1-comet-evaluator-request-queue
    design_evaluator_request_queue_url = models.TextField(null=True)
    design_evaluator_response_queue_name = models.TextField(null=True)  # user-1-comet-evaluator-response-queue
    design_evaluator_response_queue_url = models.TextField(null=True)

    # --> Genetic Algorithm
    genetic_algorithm_instance_count = models.IntegerField(default=0)
    genetic_algorithm_request_queue_name = models.TextField(null=True)  # user-1-comet-algorithm-request-queue
    genetic_algorithm_request_queue_url = models.TextField(null=True)
    genetic_algorithm_response_queue_name = models.TextField(null=True)  # user-1-comet-algorithm-response-queue
    genetic_algorithm_response_queue_url = models.TextField(null=True)




