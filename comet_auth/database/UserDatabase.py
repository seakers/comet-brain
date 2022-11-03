
# --> Tables
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from comet_assistant.models import DialogueHistory, UserAction
from comet_auth.models import UserInformation
from comet_problem.models import Problem, UserProblem, Architecture, Objective, ObjectiveValue, Parameter, Decision, Alternative, UserDataset, Dataset



from comet_problem.database.ProblemDatabase import ProblemDatabase







class UserDatabase:

    def __init__(self, user_info):
        self.user_info = user_info
        self.problem_db = ProblemDatabase(user_info=user_info)



    def get_userdata(self):
        userdata = {
            'username': self.user_info.user.username,
            'email': self.user_info.user.email,
            'pk': self.user_info.user.id,
            'user_info_pk': self.user_info.id,
            'evaluation_queue': self.user_info.design_evaluator_request_queue_url,
            'problem_id': self.user_info.problem_id,
            'dataset_id': self.user_info.dataset_id
        }
        return userdata

    def clone_problem(self):
        problem_id, dataset_id = self.problem_db.clone()
        self.user_info.problem_id = problem_id
        self.user_info.dataset_id = dataset_id
        self.user_info.save()


    @staticmethod
    def index_roles():
        from comet_auth.database.user_roles import roles
        for role in roles:
            if not User.objects.filter(username=role['name']).filter(email=role['email']).exists():
                user = User.objects.create_user(role['name'], role['email'], role['password1'])
            else:
                user = User.objects.get(username=role['name'])
            user.save()

            if not UserInformation.objects.filter(user=user).exists():
                user_info = UserDatabase.create_role_user_info(user)
            else:
                user_info = UserInformation.objects.get(user=user)
            user_info.save()



        return 0


    @staticmethod
    def create_role_user_info(role_user):
        if not UserInformation.objects.filter(user=role_user):
            user_info = UserInformation(user=role_user)
        else:
            user_info = UserInformation.objects.get(user=role_user)
        user_info.save()
        problem_db = ProblemDatabase(user_info=user_info, new_dataset=role_user.username)
        return user_info





    @staticmethod
    def clean_all():
        for user_info in UserInformation.objects.all():

            if user_info.user:
                print('--> DELETING USER', user_info.user.username)
            else:
                print('--> DELETING USER', user_info.session.session_key)

            if Architecture.objects.filter(user_information=user_info).exists():
                for arch in Architecture.objects.filter(user_information=user_info):
                    arch.delete()
            if UserAction.objects.filter(user_information=user_info).exists():
                for action in UserAction.objects.filter(user_information=user_info):
                    action.delete()
            if DialogueHistory.objects.filter(user_information=user_info).exists():
                for diag in DialogueHistory.objects.filter(user_information=user_info):
                    diag.delete()
            if UserDataset.objects.filter(user_information=user_info).exists():
                for diag in UserDataset.objects.filter(user_information=user_info):
                    diag.delete()
            if UserProblem.objects.filter(user_information=user_info).exists():
                for diag in UserProblem.objects.filter(user_information=user_info):
                    diag.delete()
            if user_info.user:
                user = user_info.user
                user_info.delete()
                user.delete()
            else:
                user_info.delete()





























