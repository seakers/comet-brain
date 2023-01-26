import datetime
import json
from django.conf import settings

from comet_assistant.assistant.intents.ParameterExtractor import ParameterExtractor
from comet_assistant.assistant.roles.Engineer import Engineer
from comet_assistant.models import DialogueHistory
from comet_auth.database.UserDatabase import UserDatabase


class IntentHandler:


    def __init__(self, user_info, command, intent):
        self.app_path = settings.COMET_PATH
        self.user_info = user_info
        self.command = command
        self.command_processed = settings.NLP_MODEL(self.command.strip())
        self.intent = intent
        self.extractor = ParameterExtractor(self.user_info, self.command_processed)
        self.user_db = UserDatabase(user_info)

    def process(self):
        intent_func = 'intent_' + str(self.intent)
        if hasattr(self, intent_func):
            print('--> PROCESSING INTENT FUNCTION:', intent_func)
            func = getattr(self, intent_func)
            result = func()
        else:
            raise Exception("Intent function DNE:", intent_func)


    ########################
    ### Intent Functions ###
    ########################
    # ["Analyst", "Engineer", "Critic", "Historian", "Teacher"]

    def insert_msg(self, message, type, writer, more_info=None):
        dialogue_piece = DialogueHistory(user_information=self.user_info, date=datetime.datetime.now(), message=message,
                                         message_type=type, message_writer=writer, more_info=more_info)
        dialogue_piece.save()

    def intent_1000(self):
        self.insert_msg('intent_1000', '1000', 'Analyst')

    def intent_1001(self):
        # --> User asks about a parameter of the design

        # --> 1. Extract features
        parameter_name = self.extractor.coarse_feature_search_by_type('parameter_name', num_features=1)
        print(parameter_name)
        if len(parameter_name) == 0:
            raise Exception("Error parsing parameters: intent_1001")
        parameter_name = str(parameter_name[0])
        parameter = self.user_db.problem_db.get_parameter(parameter_name)
        print(parameter)
        if not parameter:
            raise Exception("Error getting parameter name: intent_1001")

        message = parameter_name + ' is ' + parameter.value + parameter.units
        self.insert_msg(message, '1001', 'Analyst')

    def intent_2000(self):
        self.insert_msg('intent_2000', '2000', 'Engineer')

    def intent_2001(self):

        # --> 1. Extract features
        design_id = self.extractor.coarse_feature_search_by_type('design_id', num_features=1)
        objective_name = self.extractor.coarse_feature_search_by_type('objective_name', num_features=1)
        if len(design_id) == 0 or len(objective_name) == 0:
            raise Exception("Error parsing parameters: intent_2001")
        design_id = int(design_id[0])
        objective_name = objective_name[0]

        # --> 2. Call engineer
        report = Engineer(self.user_info).improve_design_objective(design_id, objective_name)
        print('--> ENGINEER REPORT:', report)
        message = ''
        if report['running'] is False:
            message = 'I was able to improve ' + objective_name + ' by ' + str(report['improvement'])
            message += (' by changing the following design variables: ' + report['target_rep'] + ' --> ' + report['new_design_rep'])
        else:
            message = 'I was not able to improve on the original ' + objective_name + ' score of ' + str(report['target_value']) + ' for design ' + report['target_rep'] + ' over ' + str(report['nfe']) + 'nfe'
        print('\n'+message+'\n')

        # --> 3. Insert response
        self.insert_msg(message, '2001', 'Engineer', more_info=json.dumps(report))




    def intent_3000(self):
        self.insert_msg('intent_3000', '3000', 'Critic')

    def intent_4000(self):
        self.insert_msg('intent_4000', '4000', 'Historian')

    def intent_5000(self):
        message = 'Delta-V is a measure of the impulse per unit of spacecraft mass that is needed to perform a maneuver'
        self.insert_msg(message, '5000', 'Teacher')






