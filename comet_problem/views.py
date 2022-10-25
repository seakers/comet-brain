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




class LoadProblem(APIView):

    def post(self, request, format=None):
        return Response({'status': 'success'})















