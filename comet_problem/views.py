import json
import os


from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from comet_auth.helpers import get_or_create_user_information
from comet_auth.models import UserInformation


from comet_problem.datamining.DataMining import DataMining


def to_map(data):
    if isinstance(data, list):
        return [to_map(x) for x in data]
    elif isinstance(data, dict):
        return {to_map(key): to_map(val) for key, val in data.items()}
    elif isinstance(data, int) and not isinstance(data, bool):
        return data
    else:
        return str(data)




class RunDataMining(APIView):

    def post(self, request, format=None):

        user_info = get_or_create_user_information(request.session, request.user)
        arch_ids = json.loads(request.data["arch_ids"])
        print(type(arch_ids), arch_ids)
        arch_ids = [int(x) for x in arch_ids]

        client = DataMining(user_info, arch_ids)
        itemsets, rules = client.run()
        t_rules = [{'lhs': list(rule.lhs), 'rhs': list(rule.rhs)} for rule in rules]


        return Response({
            'status': 'success',
            'rules': json.dumps(t_rules),
            'itemsets': json.dumps(to_map(itemsets))
        })






















