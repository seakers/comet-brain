from comet_auth.models import UserInformation
from comet_problem.models import Problem, UserProblem, Architecture, Objective, ObjectiveValue





def get_problem(name):
    if not Problem.objects.filter(name=name).exists():
        raise Exception("PROBLEM NOT INDEXED", name)
    else:
        return Problem.objects.get(name=name)

def add_user_to_problem(user_info, name):
    problem = get_problem(name=name)
    if not UserProblem.objects.filter(user_information=user_info).filter(problem=problem).exists():
        user_problem = UserProblem(user_information=user_info, problem=problem)
        user_problem.save()
