from django.conf import settings
from comet_auth.database.UserDatabase import UserDatabase
from comet_problem.aws.clients.SqsClient import SqsClient
from comet_problem.models import Architecture, Problem, Objective, ObjectiveValue
from asgiref.sync import async_to_sync, sync_to_async

import random
import time





class Engineer:


    def __init__(self, user_info):
        self.user_db = UserDatabase(user_info)



    def improve_design_objective(self, design_id, objective_name):
        problem = self.user_db.problem_db.problem
        if not Architecture.objects.filter(id=design_id).exists():
            raise Exception("--> INCORRECT PARAMETER EXTRACTION")
        arch = Architecture.objects.get(id=design_id)

        # --> 1. Extract target objective
        target_objective = None
        for objective in Objective.objects.filter(problem=problem):
            optimization = objective.optimization
            if objective.name == objective_name and ObjectiveValue.objects.filter(architecture=arch).filter(objective=objective).exists():
                obj_val = ObjectiveValue.objects.get(architecture=arch, objective=objective)
                objective_value = obj_val.value
                target_objective = {'id': objective.id, 'value': objective_value, 'optimization': optimization, 'name': objective.name, 'obj': objective}
        # print(objective_name, target_objective)
        if not target_objective:
            raise Exception("--> INCORRECT PARAMETER EXTRACTION")

        # --> 2. Run optimization algorithm
        return self.small_neighborhood_algorithm(target_objective, arch)


    ##################
    ### Algorithms ###
    ##################

    def small_neighborhood_algorithm(self, target_objective, initial_design, nfe_max=10):
        nfe = 0
        running = True
        target_value = target_objective['value']
        optimization = target_objective['optimization']
        objective = target_objective['obj']
        current_pop = [initial_design]
        current_pop_values = [ObjectiveValue.objects.get(architecture=initial_design, objective=objective).value]
        eval_design = None
        new_design = None
        new_design_id = None
        new_obj_value = None

        while nfe < nfe_max and running:
            new_design = self.small_neighborhood_generator(current_pop)
            user_info = self.user_db.user_info
            async_to_sync(SqsClient.send_eval_msg)(user_info.design_evaluator_request_queue_url, new_design, user_info.dataset_id, 'Engineer')
            eval_design = self.subscribe_to_arch(new_design)
            new_design_id = eval_design.id
            current_pop.append(eval_design)
            new_obj_value = ObjectiveValue.objects.get(architecture=eval_design, objective=objective).value
            current_pop_values.append(new_obj_value)
            if optimization == 'max':
                if new_obj_value > target_value:
                    running = False
            else:
                if new_obj_value < target_value:
                    running = False
            nfe += 1

        report = {
            'nfe': nfe,
            'nfe_max': nfe_max,
            'running': running,
            'target_rep': initial_design.representation,
            'new_design_rep': new_design,
            'new_design_id': new_design_id,
            'current_pop': [arch.representation for arch in current_pop],
            'current_pop_values': current_pop_values,
            'optimization': optimization,
            'target_value': target_value,
            'new_obj_value': new_obj_value,
            'improvement': round(abs(new_obj_value - target_value), 5)
        }
        return report




    ##################
    ### Generators ###
    ##################


    def small_neighborhood_generator(self, current_pop):
        decisions = self.user_db.problem_db.get_problem_decisions()
        arch = random.choice(current_pop)
        rep_str = arch.representation
        rep_list = self.str_to_list(rep_str)

        novel_arch = 0
        mut_prob = 1.0 / len(decisions)
        max = 100
        counter = 0
        mut_str = rep_str
        while novel_arch is not None and counter < max:
            mut_list = []
            for idx, val in enumerate(rep_list):
                if random.random() < mut_prob:
                    mut_list.append(random.randint(0, len(decisions[idx]['alternatives'])-1))
                else:
                    mut_list.append(rep_list[idx])
            mut_str = self.list_to_str(mut_list)
            novel_arch = self.user_db.problem_db.get_problem_design(mut_str)
            time.sleep(0.05)
            counter += 1
        if counter >= max:
            raise Exception('Could not generate novel design: small_neighborhood_generator')
        return mut_str















    ###############
    ### Helpers ###
    ###############

    def str_to_list(self, int_str):
        return [int(x) for x in int_str]

    def list_to_str(self, int_list):
        build = ''
        for x in int_list:
            build += str(x)
        return build


    def subscribe_to_arch(self, representation):
        counter = 0
        max = 150
        while counter < max:
            design = self.user_db.problem_db.get_problem_design(representation)
            if design is not None:
                return design
            time.sleep(2)
            counter += 1
        raise Exception("--> ARCH WAS NEVER EVALUATED")



