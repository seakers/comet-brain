from django.core.management.base import BaseCommand, CommandError
from comet_problem.database.ProblemDatabase import ProblemDatabase


class Command(BaseCommand):
    help = 'Index comet database'

    def handle(self, *args, **options):
        print('--> INDEXING DATABASE')
        ProblemDatabase.insert_default()

