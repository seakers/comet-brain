from django.conf import settings

from comet_assistant.assistant.intents.ParameterExtractor import ParameterExtractor


class IntentHandler:


    def __init__(self, user_info, command, intent):
        self.app_path = settings.COMET_PATH
        self.user_info = user_info
        self.command = command
        self.command_processed = settings.NLP_MODEL(self.command.strip())
        self.intent = intent
        self.extractor = ParameterExtractor(self.user_info, self.command_processed)

    def process(self):
        intent_func = 'intent_' + str(self.intent)
        if hasattr(self, intent_func):
            print('--> PROCESSING INTENT FUNCTION:', intent_func)
            func = getattr(self, intent_func)
            func()
        else:
            raise Exception("--> INTENT FUNCTION DOES NOT EXIST:", intent_func)

    def intent_1000(self):
        print('--> intent_1000')

    def intent_2000(self):
        print('--> intent_2000')

    def intent_3000(self):
        print('--> intent_3000')

    def intent_4000(self):
        print('--> intent_4000')

    def intent_5000(self):
        print('--> intent_5000')






