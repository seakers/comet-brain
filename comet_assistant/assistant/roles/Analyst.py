from django.conf import settings
from comet_auth.database.UserDatabase import UserDatabase
from comet_problem.aws.clients.SqsClient import SqsClient
from comet_problem.datamining.DataMining import DataMining
from comet_problem.models import Architecture, Problem, Objective, ObjectiveValue
from asgiref.sync import async_to_sync, sync_to_async

import random
import time

from paretoset import paretoset
import pandas as pd



class Analyst:


    def __init__(self, user_info):
        self.user_info = user_info
        self.user_db = UserDatabase(user_info)



    def get_pareto_front(self, designs=None):
        if designs is None:
            designs = self.user_db.problem_db.get_dataset_designs()

        designs_dict = {}
        objective_rows = []
        name_array = []
        opt_array = []
        for design in designs:
            obj_info = self.user_db.problem_db.get_design_objectives(design.id)
            obj_array = [x['value'] for x in obj_info]
            name_array = [x['name'] for x in obj_info]
            opt_array = [x['optimization'] for x in obj_info]
            objective_rows.append(obj_array)
            designs_dict[design.id] = obj_array

        dataframe_dict = {}
        for name in name_array:
            dataframe_dict[name] = []
        for row in objective_rows:
            for idx, val in enumerate(row):
                name = name_array[idx]
                dataframe_dict[name].append(val)

        df = pd.DataFrame(dataframe_dict)
        mask = paretoset(df, opt_array)
        pareto_designs = []
        for idx, mval in enumerate(mask):
            if bool(mval) is True:
                pareto_designs.append(designs[idx])

        # print(pareto_designs)
        return pareto_designs


    def get_driving_features(self):


        # --> Get designs in pareto front
        pareto_designs = self.get_pareto_front()
        pareto_ids = [x.id for x in pareto_designs]
        # print(pareto_ids)


        client = DataMining(self.user_info, selected_ids=pareto_ids)
        itemsets, rules = client.run()
        return itemsets, rules




