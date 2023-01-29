import time

from django.core.management.base import BaseCommand, CommandError

from comet_assistant.assistant.Classifier import Classifier

from comet_assistant.assistant.intents.IntentHandler import IntentHandler
from comet_auth.models import UserInformation

from comet_problem.datamining.DataMining import DataMining


class Command(BaseCommand):
    help = 'Creates training data for comet models'

    def handle(self, *args, **options):
        print('--> TESTING DATAMINING API')
        user_info_id = 13
        user_info = UserInformation.objects.get(id=user_info_id)

        client = DataMining(user_info)
        results = client.run()












