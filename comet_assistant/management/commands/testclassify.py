import time

from django.core.management.base import BaseCommand, CommandError

from comet_assistant.assistant.Classifier import Classifier

from comet_assistant.assistant.intents.IntentHandler import IntentHandler
from comet_auth.models import UserInformation


class Command(BaseCommand):
    help = 'Creates training data for comet models'

    def handle(self, *args, **options):
        command = 'how can design 1963 improve EPS Mass?'


        print('--> TEST COMMAND CLASSIFICATION:', command)
        start = time.time()

        classifier = Classifier()
        print('--> CONSTRUCTOR: ', time.time() - start)


        role_result = classifier.classify_role(command)
        print('--> ROLE:', classifier.get_role(role_result), time.time() - start)

        intent_result = classifier.classify_role_intent(command, role_result)
        intent = classifier.get_intent(role_result, intent_result)
        print('--> INTENT:', intent, time.time() - start)

        user_info_id = 38
        user_info = UserInformation.objects.get(id=user_info_id)
        intent_handler = IntentHandler(user_info, command, intent)
        intent_handler.process()











