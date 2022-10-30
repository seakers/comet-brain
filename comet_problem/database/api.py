from django.db import transaction
from asgiref.sync import SyncToAsync, sync_to_async

# --> Tables
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from comet_auth.models import UserInformation
from comet_problem.models import Problem, UserProblem, Architecture, Objective, ObjectiveValue

from comet_problem.default import default_problem

class DatabaseAPI:

    def __init__(self, user_info):
        self.user_info = user_info

        # --> Default Problem
        self.default_problem = default_problem


    def get_default_problem(self):
        problem_name = default_problem['name']
        if not Problem.objects.filter(name=problem_name).exists():
            raise Exception("--> Default Problem DNE", problem_name)
        else:
            return Problem.objects.get(name=problem_name)

    def get_problem(self, problem_name=None, problem_id=None):
        if problem_name:
            if not Problem.objects.filter(name=problem_name).exists():
                raise Exception("--> Problem DNE", problem_name)
            else:
                return Problem.objects.get(name=problem_name)
        elif problem_id:
            if not Problem.objects.filter(id=problem_id).exists():
                raise Exception("--> Problem DNE", problem_id)
            else:
                return Problem.objects.get(id=problem_id)
        else:
            raise Exception("--> INVALID PARAMETERS")



    def add_user_to_problem(self, problem_id):
        problem = self.get_problem(problem_id=problem_id)
        if not UserProblem.objects.filter(user_information=self.user_info).filter(problem=problem).exists():
            user_problem = UserProblem(user_information=self.user_info, problem=problem)
            user_problem.save()




        # --> Insert: UserProblem table (set user current problem)
        # --> Insert: Dataset table     (set user current dataset)
        return None






