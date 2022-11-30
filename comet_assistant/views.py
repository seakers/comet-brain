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
from comet_assistant.assistant.Classifier import Classifier




class Command(APIView):

    def post(self, request, format=None):

        user_info = get_or_create_user_information(request.session, request.user)

        command = request.data["command"]
        print('--> PROCESSING COMMAND: ', command)
        classifier = Classifier()

        role_result = classifier.classify_role(command)
        print('--> ROLE: ', classifier.get_role(role_result))

        intent_result = classifier.classify_role_intent(command, role_result)
        print('--> INTENT:', intent_result)

        return Response({'status': 'success'})















