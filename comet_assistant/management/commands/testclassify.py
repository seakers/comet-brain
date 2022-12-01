import time

from django.core.management.base import BaseCommand, CommandError

from comet_assistant.assistant.Classifier import Classifier

class Command(BaseCommand):
    help = 'Creates training data for comet models'

    def handle(self, *args, **options):
        print('--> TEST COMMAND CLASSIFICATION')
        start = time.time()

        classifier = Classifier()
        print('--> CONSTRUCTOR: ', time.time() - start)

        command = 'what are the strengths of design 5?'

        role_result = classifier.classify_role(command)
        print('--> ROLE:', classifier.get_role(role_result), time.time() - start)

        intent_result = classifier.classify_role_intent(command, role_result)
        print('--> INTENT:', classifier.get_intent(role_result, intent_result), time.time() - start)








