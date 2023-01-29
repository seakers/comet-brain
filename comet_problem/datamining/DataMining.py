import os
from comet_assistant.assistant.roles.Engineer import Engineer

from comet_auth.database.UserDatabase import UserDatabase
from efficient_apriori import apriori

from comet_problem.models import ObjectiveValue


class DataMining:

    def __init__(self, user_info, selected_ids=None):
        self.user_info = user_info
        self.selected_ids = selected_ids
        self.user_db = UserDatabase(user_info)

        # --> Problem Info

        # --> Build info
        self.decisions = {}
        self.all_archs = {}
        self.build()

    def build(self):

        # --> 1. Get problem decisions
        self.decisions = self.user_db.problem_db.get_problem_decisions()

        # --> 2. Get designs and filter
        all_archs = self.user_db.problem_db.get_dataset_designs()
        all_archs = self.filter_archs(all_archs)

        # --> 3. Parse designs into data-mining form
        for arch in all_archs:
            parse_result = self.parse_arch_elements(arch)
            self.all_archs[arch.id] = parse_result

    def filter_archs(self, all_archs):
        filtered_archs = []
        for arch in all_archs:
            if arch.evaluation_status is False:
                continue
            if not self.selected_ids:
                filtered_archs.append(arch)
            else:
                if arch.id in self.selected_ids:
                    filtered_archs.append(arch)
        return filtered_archs

    def parse_arch_elements(self, arch):
        representation = Engineer.str_to_list(arch.representation)

        # --> 1. Ensure every item in inputs is of type int
        inputs = [int(input) for input in representation]

        # --> 2. Parse inputs into design vector
        design = []
        for idx, input in enumerate(inputs):
            decision_name = self.decisions[idx]['name']
            decision_value = self.decisions[idx]['alternatives'][input]['value']
            decision_label = '(' + decision_name + ', ' + decision_value + ')'
            design.append(decision_label)
            # if idx == 0:
            #     design.append(decision_value)
            # elif idx == 1:
            #     design.append(decision_value)
            # elif idx == 2:
            #     design.append(decision_value)
            # elif idx == 3:
            #     design.append(str(decision_value + '-panels'))
            # elif idx == 4:
            #     design.append(str(decision_value+'-dof'))
            # elif idx == 5:
            #     design.append(str(decision_value+'-norm'))

        # print('-->', representation, design)
        return design

    def run(self):
        print('--> FINDING ASSOCIATION RULES')

        inputs = []
        # --> 1. Create list of tuples
        for key, value in self.all_archs.items():
            inputs.append(tuple(value))

        itemsets, rules = self.mine_features(inputs)
        return itemsets, rules

    def mine_features(self, data_set):
        support_values = [(x + 1) * 0.1 for x in range(1, 10)]
        for val in support_values:
            # print('--> SUPPORT VAL:', round(val, 1))
            correct_val = False
            try:
                itemsets, rules = apriori(data_set, min_support=val, min_confidence=1)
                # print('--> RESULT RULES:', round(val, 1), rules)
                return itemsets, rules
            except Exception as ex:
                continue
        return []
