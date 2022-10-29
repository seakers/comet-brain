from django.core.management.base import BaseCommand, CommandError

from comet_assistant.assistant.Classifier import Classifier

class Command(BaseCommand):
    help = 'Creates training data for comet models'

    def handle(self, *args, **options):
        print('--> CREATING TRAINING DATA')
        classifier = Classifier()

        command = 'what are the driving features'









