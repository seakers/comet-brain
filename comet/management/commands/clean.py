from django.core.management.base import BaseCommand, CommandError


# --> Database Imports
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from comet_auth.models import UserInformation
from comet_assistant.models import DialogueHistory, Action, UserAction
from comet_problem.models import Problem, UserProblem, Architecture, Objective, ObjectiveValue, Parameter, Decision, Alternative

# --> Default Problem
from comet_problem.default import default_problem



class Command(BaseCommand):
    help = 'Clean comet database'

    def handle(self, *args, **options):
        print('--> CLEANING DATABASE')

        # --> 1. Get or insert default problem
        self.delete_parameters()


    def delete_parameters(self):
        name = default_problem['name']
        if Problem.objects.filter(name=name).exists():
            problem = Problem.objects.get(name=name)
            parameters = default_problem['parameters']
            for parameter in parameters:
                if Parameter.objects.filter(problem=problem).filter(name=parameter['name']).exists():
                    entry = Parameter.objects.get(problem=problem, name=parameter['name'])
                    entry.delete()

    def delete_objectives(self):
        name = default_problem['name']
        if Problem.objects.filter(name=name).exists():
            problem = Problem.objects.get(name=name)
            objectives = default_problem['objectives']
            for objective in objectives:
                if Objective.objects.filter(problem=problem).filter(name=objective[0]).exists():
                    entry = Objective.objects.get(problem=problem, name=objective[0], type=objective[1])
                    entry.delete()
