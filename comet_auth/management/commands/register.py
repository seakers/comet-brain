import time

from django.core.management.base import BaseCommand, CommandError

from comet_assistant.assistant.Classifier import Classifier

from comet_assistant.assistant.intents.IntentHandler import IntentHandler
from comet_auth.models import UserInformation

from comet_problem.datamining.DataMining import DataMining




class Command(BaseCommand):
    help = 'Registers a user'

    def handle(self, *args, **options):
        print('--> TESTING USER REGISTRATION')
