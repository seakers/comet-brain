from django.db import transaction
from asgiref.sync import SyncToAsync, sync_to_async

# --> Tables
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from comet_auth.models import UserInformation
from comet_problem.models import Problem, UserProblem, Architecture, Objective, ObjectiveValue, Parameter, Decision, Alternative, UserDataset, Dataset

from comet_problem.default import default_problem




class ProblemDatabase:

    def __init__(self, user_info=None, problem=None, new_dataset=None):
        self.user_info = user_info
        self.problem = problem
        self.new_dataset = new_dataset
        if not problem:
            self.problem = self.get_problem()


    def get_problem(self):
        if self.user_info:
            if self.user_info.problem_id is None:
                if self.new_dataset:
                    self.add_user_to_default_problems()
                else:
                    self.add_user_to_all_problems(new_dataset=self.new_dataset)
            if Problem.objects.filter(id=self.user_info.problem_id).exists():
                return Problem.objects.get(id=self.user_info.problem_id)
            else:
                raise Exception("--> PROBLEM DOES NOT EXIST")
        else:
            return self.get_default_problems()[0]


    def add_user_to_all_problems(self, new_dataset=None):
        for problem in Problem.objects.all():
            problem_id, dataset_id = self.add_user_to_problem(problem, new_dataset)
        self.user_info.problem_id = problem_id
        self.user_info.dataset_id = dataset_id
        self.user_info.save()


    def add_user_to_default_problems(self, new_dataset=None):
        problem_id, dataset_id = None, None
        for problem in self.get_default_problems():
            problem_id, dataset_id = self.add_user_to_problem(problem, new_dataset)
        self.user_info.problem_id = problem_id
        self.user_info.dataset_id = dataset_id
        self.user_info.save()

    def get_default_problems(self):
        if Problem.objects.filter(default=True).exists():
            return Problem.objects.filter(default=True)
        else:
            return ProblemDatabase.insert_default()

    def add_user_to_problem(self, problem=None, new_dataset=None):

        # --> 1. Add user to problem
        if not problem:
            problem = self.problem
        if not UserProblem.objects.filter(user_information=self.user_info).filter(problem=problem):
            user_problem = UserProblem(user_information=self.user_info, problem=problem, owner=False)
            user_problem.save()

        # --> 2. Add user to default dataset
        if new_dataset is None:
            default_dataset = self.get_default_dataset(problem=problem)
            if not UserDataset.objects.filter(user_information=self.user_info).filter(dataset=default_dataset).exists():
                user_dataset = UserDataset(user_information=self.user_info, dataset=default_dataset, owner=False)
                user_dataset.save()
            return problem.id, default_dataset.id
        else:
            # Create new dataset
            if not Dataset.objects.filter(problem=problem, name=new_dataset, default=False):
                new_dataset = Dataset.objects.get(problem=problem, name=new_dataset, default=False)
            else:
                new_dataset = Dataset(problem=problem, name=new_dataset, default=False)
            new_dataset.save()

            if not UserDataset.objects.filter(user_information=self.user_info).filter(dataset=new_dataset).exists():
                user_dataset = UserDataset(user_information=self.user_info, dataset=new_dataset, owner=True)
            else:
                user_dataset = UserDataset.objects.get(user_information=self.user_info, dataset=new_dataset)
            user_dataset.save()
            return problem.id, new_dataset.id

    def get_default_dataset(self, problem=None):
        if not problem:
            problem = self.problem
        if Dataset.objects.filter(problem=problem).filter(default=True).exists():
            return Dataset.objects.get(problem=problem, default=True)
        else:
            raise Exception("--> DEFAULT DATASET DOESNT EXIST FOR PROBLEM")

    ##############
    ### Insert ###
    ##############
    # Requires: default_problem

    @staticmethod
    def insert_default():
        return ProblemDatabase.insert(default_problem)

    @staticmethod
    def insert(problem_definition):
        print('--> INSERTING PROBLEM:', problem_definition['name'])
        problem = ProblemDatabase.insert_problem(problem_definition)
        ProblemDatabase.insert_parameters(problem, problem_definition)
        ProblemDatabase.insert_decisions(problem, problem_definition)
        ProblemDatabase.insert_objectives(problem, problem_definition)
        ProblemDatabase.insert_dataset(problem, problem_definition)
        return problem

    @staticmethod
    def insert_problem(problem_definition):
        name = problem_definition['name']
        if Problem.objects.filter(name=name).exists():
            problem = Problem.objects.get(name=name)
        else:
            problem = Problem(name=name, default=True)
            problem.save()
        return problem

    @staticmethod
    def insert_dataset(problem, problem_definition):
        if not Dataset.objects.filter(problem=problem).filter(name=problem_definition['dataset']['name']).exists():
            entry = Dataset(problem=problem, name=problem_definition['dataset']['name'], default=True)
            entry.save()

    @staticmethod
    def insert_objectives(problem, problem_definition):
        objectives = problem_definition['objectives']
        for objective in objectives:
            if not Objective.objects.filter(problem=problem).filter(name=objective['name']).exists():
                entry = Objective(problem=problem, name=objective['name'], type=objective['type'], optimization=objective['optimization'], bounds=objective['bounds'])
                entry.save()

    @staticmethod
    def insert_parameters(problem, problem_definition):
        parameters = problem_definition['parameters']
        for parameter in parameters:
            if not Parameter.objects.filter(problem=problem).filter(name=parameter['name']).exists():
                entry = Parameter(problem=problem, name=parameter['name'], units=parameter['units'],
                                  type=parameter['type'], value=parameter['value'])
                entry.save()

    @staticmethod
    def insert_decisions(problem, problem_definition):
        decisions = problem_definition['decisions']
        for decision in decisions:
            if not Decision.objects.filter(problem=problem).filter(name=decision['name']).exists():
                decision_entry = Decision(problem=problem, name=decision['name'], type=decision['type'])
                decision_entry.save()
            else:
                decision_entry = Decision.objects.get(problem=problem, name=decision['name'])

            alternatives = decision['alternatives']
            for alternative in alternatives:
                if not Alternative.objects.filter(decision=decision_entry).filter(
                        value=alternative['value']).exists():
                    alternative_entry = Alternative(decision=decision_entry, value=alternative['value'],
                                                    description=alternative['description'])
                    alternative_entry.save()




    @staticmethod
    def insert_role_datasets():
        from comet_auth.database.user_roles import roles
        for role in roles:
            for problem in Problem.objects.all():
                if not Dataset.objects.filter(problem=problem).filter(name=role['dataset']):
                    dataset = Dataset(problem=problem, name=role['dataset'], default=False)
                    dataset.save()
                else:
                    dataset = Dataset.objects.get(problem=problem, name=role['dataset'])
                    


    #############
    ### Clean ###
    #############
    # Requires: problem name


    @staticmethod
    def clean_all():
        for problem in Problem.objects.all():
            ProblemDatabase(problem=problem).clean()


    def clean(self):

        # --> Order of deletion
        self.clean_parameters()
        self.clean_decisions()
        self.clean_datasets()
        self.clean_objectives()
        self.clean_problem()

    def clean_problem(self):
        if UserProblem.objects.filter(problem=self.problem).exists():
            entries = UserProblem.objects.filter(problem=self.problem)
            for entry in entries:
                entry.delete()
        self.problem.delete()
        self.problem = None
        return None

    def clean_parameters(self):
        if Parameter.objects.filter(problem=self.problem).exists():
            entries = Parameter.objects.filter(problem=self.problem)
            for entry in entries:
                entry.delete()

    def clean_decisions(self):
        if Decision.objects.filter(problem=self.problem).exists():
            for entry in Decision.objects.filter(problem=self.problem):
                self.clean_alternatives(decision=entry)
                entry.delete()

    def clean_alternatives(self, decision=None):
        if decision:
            if Alternative.objects.filter(decision=decision).exists():
                for entry in Alternative.objects.filter(decision=decision):
                    entry.delete()

    def clean_datasets(self):
        if Dataset.objects.filter(problem=self.problem).exists():
            entries = Dataset.objects.filter(problem=self.problem)
            for entry in entries:
                self.clean_user_datasets(dataset=entry)
                self.clean_architectures(dataset=entry)
                entry.delete()

    def clean_user_datasets(self, dataset=None):
        if dataset:
            if UserDataset.objects.filter(dataset=dataset).exists():
                entries = UserDataset.objects.filter(dataset=dataset)
                for entry in entries:
                    entry.delete()
        else:
            if UserDataset.objects.exists():
                entries = UserDataset.objects.all()
                for entry in entries:
                    entry.delete()

    def clean_architectures(self, dataset=None):
        if dataset:
            if Architecture.objects.filter(problem=self.problem).filter(dataset=dataset).exists():
                entries = Architecture.objects.filter(problem=self.problem).filter(dataset=dataset)
                for entry in entries:
                    self.clean_objective_values(architecture=entry)
                    entry.delete()
        else:
            if Architecture.objects.filter(problem=self.problem).exists():
                entries = Architecture.objects.filter(problem=self.problem)
                for entry in entries:
                    self.clean_objective_values(architecture=entry)
                    entry.delete()

    def clean_objectives(self):
        if Objective.objects.filter(problem=self.problem).exists():
            entries = Objective.objects.filter(problem=self.problem)
            for entry in entries:
                self.clean_objective_values(objective=entry)
                entry.delete()

    def clean_objective_values(self, architecture=None, objective=None):
        if architecture:
            if ObjectiveValue.objects.filter(architecture=architecture).exists():
                entries = ObjectiveValue.objects.filter(architecture=architecture)
                for entry in entries:
                    entry.delete()
        if objective:
            if ObjectiveValue.objects.filter(objective=objective).exists():
                entries = ObjectiveValue.objects.filter(objective=objective)
                for entry in entries:
                    entry.delete()



    #############
    ### Clone ###
    #############
    # Requires: problem name

    def clone(self):
        problem = self.get_problem()
        clone = self.clone_problem(problem)
        self.clone_parameters(clone)
        self.clone_decisions(clone)
        self.clone_objectives(clone)
        dataset_id = self.clone_default_dataset(clone)  # Just inserts a new default dataset
        return clone.id, dataset_id

    def clone_problem(self, problem):
        problem.pk = None
        problem.save()
        return problem

    def clone_parameters(self, clone):
        if Parameter.objects.filter(problem=self.problem).exists():
            entries = Parameter.objects.filter(problem=self.problem)
            for entry in entries:
                entry.pk = None
                entry.save()
                entry.problem = clone
                entry.save()

    def clone_decisions(self, clone):
        if Decision.objects.filter(problem=self.problem).exists():
            for entry in Decision.objects.filter(problem=self.problem):

                alternatives = self.clone_alternatives(entry)

                # clone_entry = Decision(problem=clone, name=entry.name, type=entry.type)
                # clone_entry.save()

                entry.pk = None
                entry.save()
                entry.problem = clone
                entry.save()

                for alt in alternatives:
                    alt.decision = entry
                    alt.save()

    def clone_alternatives(self, clone):
        alternatives = []
        if Alternative.objects.filter(decision=clone).exists():
            for alt_entry in Alternative.objects.filter(decision=clone):
                alt_entry.pk = None
                alt_entry.save()
                alternatives.append(alt_entry)
        return alternatives

    def clone_objectives(self, clone):
        if Objective.objects.filter(problem=self.problem).exists():
            entries = Objective.objects.filter(problem=self.problem)
            for entry in entries:
                entry.pk = None
                entry.save()
                entry.problem = clone
                entry.save()

    def clone_default_dataset(self, clone_problem):
        if not Dataset.objects.filter(problem=clone_problem, default=True).exists():
            entry = Dataset(problem=clone_problem, name='Default', default=True)
            entry.save()
        else:
            entry = Dataset.objects.get(problem=clone_problem, default=True)

        if not UserDataset.objects.filter(user_information=self.user_info).filter(problem=clone_problem).filter(dataset=entry):
            ud_entry = UserDataset(user_information=self.user_info, problem=clone_problem, dataset=entry)
            ud_entry.save()
        return entry.id
