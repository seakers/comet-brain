from django.core.management.base import BaseCommand, CommandError
from comet_problem.database.ProblemDatabase import ProblemDatabase
from comet_auth.database.UserDatabase import UserDatabase

from comet_problem.models import Problem


class Command(BaseCommand):
    help = 'Clean comet database'

    def handle(self, *args, **options):
        print('--> CLEANING DATABASE')
        UserDatabase.clean_all()
        # UserDatabase.clean_all_fast()
        ProblemDatabase.clean_all()




