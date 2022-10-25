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
    help = 'Index comet database'

    def handle(self, *args, **options):
        print('--> INDEXING DATABASE')
        self.index_default_problem()





    def index_assistant(self):
        return 0



    def index_default_problem(self):

        # --> 1. Get or insert default problem
        name = default_problem['name']
        if Problem.objects.filter(name=name).exists():
            problem = Problem.objects.get(name=name)
        else:
            problem = Problem(name=name)
            problem.save()


        # --> 2. Insert problem objectives (if DNE)
        objectives = default_problem['objectives']
        for objective in objectives:
            if not Objective.objects.filter(problem=problem).filter(name=objective[0]).exists():
                entry = Objective(problem=problem, name=objective[0], type=objective[1])
                entry.save()


        # --> 3. Insert problem parameters (if DNE)
        parameters = default_problem['parameters']
        for parameter in parameters:
            if not Parameter.objects.filter(problem=problem).filter(name=parameter['name']).exists():
                entry = Parameter(problem=problem, name=parameter['name'], units=parameter['units'], type=parameter['type'], value=parameter['value'])
                entry.save()


        # --> 4. Insert problem decisions and their alternatives (if DNE)
        decisions = default_problem['decisions']
        for decision in decisions:
            if not Decision.objects.filter(problem=problem).filter(name=decision['name']).exists():
                decision_entry = Decision(problem=problem, name=decision['name'], type=decision['type'])
                decision_entry.save()
            else:
                decision_entry = Decision.objects.get(problem=problem, name=decision['name'])

            alternatives = decision['alternatives']
            for alternative in alternatives:
                if not Alternative.objects.filter(decision=decision_entry).filter(value=alternative['value']).exists():
                    alternative_entry = Alternative(decision=decision_entry, value=alternative['value'], description=alternative['description'])
                    alternative_entry.save()



        return 0





