from django.core.management.base import BaseCommand, CommandError

from comet_assistant.assistant.Classifier import Classifier

class Command(BaseCommand):
    help = 'Creates training data for comet models'

    def handle(self, *args, **options):
        print('--> TEST COMMAND CLASSIFICATION')
        classifier = Classifier()

        command = 'why does design 5 have this science score'

        result = classifier.classify_role(command)

        print(result)









