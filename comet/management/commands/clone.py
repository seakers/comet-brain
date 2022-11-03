from django.core.management.base import BaseCommand, CommandError
from comet_problem.database.ProblemDatabase import ProblemDatabase



class Command(BaseCommand):
    help = 'Clone comet problem'

    def handle(self, *args, **options):
        print('--> CLONING PROBLEM')
        database = ProblemDatabase()
        database.clone()

