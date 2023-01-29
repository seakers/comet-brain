import time
import json

from django.core.management.base import BaseCommand, CommandError

from comet_assistant.assistant.Classifier import Classifier

from comet_auth.models import UserInformation

from comet_assistant.assistant.roles.Analyst import Analyst


def to_map(data):
    if isinstance(data, list):
        return [to_map(x) for x in data]
    elif isinstance(data, dict):
        return {to_map(key): to_map(val) for key, val in data.items()}
    elif isinstance(data, int) and not isinstance(data, bool):
        return data
    else:
        return str(data)

class Command(BaseCommand):
    help = 'Tests analyst api'

    def handle(self, *args, **options):
        print('--> TESTING ANALYST API')
        user_info_id = 13
        user_info = UserInformation.objects.get(id=user_info_id)

        client = Analyst(user_info)
        itemsets, rules = client.get_driving_features()



        print(itemsets)

        t_rules = [{'lhs': list(rule.lhs), 'rhs': list(rule.rhs)} for rule in rules]
        print(t_rules)

        # for rule in rules:
        #     print('LHS:', rule.lhs, 'RHS:', rule.rhs)
        #     lhs = list(rule.lhs)
        #     rhs = list(rule.rhs)
        #     print('LHS:', lhs, 'RHS:', rhs)



        #
        # result = json.dumps(to_map(itemsets))
        # print(result)




        # print('\n---------- RULES ----------')
        # for rule in rules:
        #     print(rule)




