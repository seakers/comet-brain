from django.conf import settings
import operator
import Levenshtein as lev

from comet_auth.database.UserDatabase import UserDatabase
from comet_problem.models import Architecture, Problem, Objective


class ParameterExtractor:


    def __init__(self, user_info, command_processed):
        self.user_info = user_info
        self.user_db = UserDatabase(user_info)
        self.command_processed = command_processed
        self.parameter_types = [
            'measurement',
            'design_id',
            'objective_name'
        ]


    ########################
    ### Parameter Search ###
    ########################

    def coarse_feature_search_by_type(self, parameter_type, num_features=1, case_sensitive=False):
        obt_feature_list = self.fine_feature_search_by_type(parameter_type, case_sensitive)
        obt_feature_list = self.crop_list(obt_feature_list, num_features)
        obt_feature_list = sorted(obt_feature_list, key=lambda ratio_info: ratio_info[2])
        obt_feature_list = [feature[0] for feature in obt_feature_list]
        return obt_feature_list

    def fine_feature_search_by_type(self, parameter_type, case_sensitive=False):
        search_list = self.get_parameter_search_list(parameter_type)
        ratio_ordered = []
        length_question = len(self.command_processed.text)
        for feature in search_list:
            length_feature = len(feature)
            if length_feature > length_question:
                ratio_ordered.append((feature, 0, -1))
            else:
                substrings = [self.command_processed.text[i:i + length_feature] for i in
                              range(length_question - length_feature + 1)]
                if case_sensitive:
                    ratios = [lev.ratio(substrings[i], feature) for i in range(length_question - length_feature + 1)]
                else:
                    ratios = [lev.ratio(substrings[i].lower(), feature.lower()) for i in
                              range(length_question - length_feature + 1)]
                max_index, max_ratio = max(enumerate(ratios), key=operator.itemgetter(1))
                ratio_ordered.append((feature, max_ratio, max_index))

        # Keep the longest string by default
        ratio_ordered = sorted(ratio_ordered, key=lambda ratio_info: -len(ratio_info[0]))
        ratio_ordered = sorted(ratio_ordered, key=lambda ratio_info: -ratio_info[1])
        ratio_ordered = [ratio_info for ratio_info in ratio_ordered if ratio_info[1] > 0.75]
        return ratio_ordered





    #############################
    ### Parameter Search List ###
    #############################

    def get_parameter_search_list(self, parameter_type):
        if parameter_type not in self.parameter_types:
            raise Exception("--> Invalid parameter type")

        search_list = []
        if parameter_type == 'design_id':
            search_list = self.get_design_ids()
        elif parameter_type == 'measurement':
            search_list = self.get_measurements()
        elif parameter_type == 'objective_name':
            search_list = self.get_objective_names()
        return search_list

    def get_design_ids(self):
        problem = Problem.objects.get(id=self.user_info.problem_id)
        design_ids = []
        for arch in Architecture.objects.filter(problem=problem):
            design_ids.append(str(arch.id))
        return design_ids

    def get_objective_names(self):
        problem = self.user_db.problem_db.problem
        objective_names = []
        for objective in Objective.objects.filter(problem=problem):
            objective_names.append(objective.name)
        return objective_names

    def get_measurements(self):
        return []



    ############################
    ### Parameter Validation ###
    ############################

    def validate_objective_names(self):
        return 0

    def validate_design_ids(self):
        return 0





    ###############
    ### Helpers ###
    ###############

    def crop_list(self, full_list, max_size):
        if len(full_list) > max_size:
            return full_list[:max_size]
        else:
            return full_list






