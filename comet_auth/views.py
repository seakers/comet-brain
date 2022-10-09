import json
import os

from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync, sync_to_async



# from comet_auth.helpers import get_or_create_user_information
# from daphne_context.models import UserInformation




class Register(APIView):
    """
    Register a user
    """
    username_blacklist = ['default']

    def post(self, request, format=None):


        # # --> 1. Extract fields
        # username = request.data["username"]
        # email = request.data["email"]
        # password1 = request.data["password1"]
        # password2 = request.data["password2"]
        # daphne_version = request.data['daphneVersion']
        #
        #
        # # --> 2. Validate fields
        # validation = self.validate(username, email, password1, password2)
        # if validation is not None:
        #     return validation
        #
        #
        # # --> 3. Create user / insert into default group
        # try:
        #     user_id = self.create_user(username, email, password1)
        #     async_to_sync(AbstractGraphqlClient.add_user_to_group)(user_id, 1)
        # except ValueError:
        #     return Response({'status': 'registration_error', 'registration_error': 'Error creating user!'})
        #
        #
        # # --> 4. Authenticate registered user
        # user = authenticate(request, username=username, password=password1)
        # if user is None:
        #     return Response({'status': 'auth_error', 'login_error': 'Invalid Credentials'})
        #
        #
        # # --> 5. Create user info / transfer session
        # userinfo = self.get_user_info_wrapper(user, request, daphne_version)
        #
        #
        # # --> 6. Log user in
        # login(request, user)
        #
        #
        # # --> 7. Initialize services
        # def init_service(service_manager):
        #     async_to_sync(service_manager.initialize)(blocking=True)
        # service_manager = ServiceManager(userinfo)
        # thread = threading.Thread(target=init_service, args=(service_manager,))
        # thread.start()
        #
        #
        #
        # # --> 8. Return
        # return Response({
        #     'status': 'logged_in',
        #     'username': username,
        #     'pk': get_user_pk(username),
        #     'is_experiment_user': userinfo.is_experiment_user,
        #     'permissions': []
        # })
        return Response({
            'status': 'logged_in',
            'username': 'gapaza',
            'pk': '1'
        })



    # --> TODO: Add logic so only pre-validated users can register. Saving resources
    def validate(self, username, email, password1, password2):

        # --> Validate email
        try:
            validate_email(email)
        except ValidationError:
            return Response({
                'status': 'registration_error',
                'registration_error': 'Email has an incorrect format.'
            })

        # --> Validate password
        if not password1 or not password2 or password1 != password2:
            return Response({
                'status': 'registration_error',
                'registration_error': 'The passwords do not match.'
            })

        # --> Validate username isn't blacklisted
        if username in self.username_blacklist:
            return Response({
                'status': 'registration_error',
                'registration_error': 'This username is already in use.'
            })

        # --> Validate username uniqueness
        if User.objects.filter(username=username).exists():
            return Response({
                'status': 'registration_error',
                'registration_error': 'This username is already in use.'
            })

    def create_user(self, username, email, password):
        user = User.objects.create_user(username, email, password)
        user.save()
        return user.id

    def get_user_info_wrapper(self, user, request, daphne_version):
        userinfo = None

        # # --> 1. Check if user_info object exists for user
        # # - if user_info exists, set daphne_version and return
        # # - if user_info dne, call get_or_create_user_information to create... then transfer current session
        # query = UserInformation.objects.filter(user__exact=user)
        # if len(query) > 0:
        #     # --> If UserInformation exists (return first)
        #     userinfo = query.first()
        #     userinfo.daphne_version = daphne_version
        #     userinfo.save()
        # else:
        #     # --> If UserInformation DNE (create UserInformation)
        #     userinfo = get_or_create_user_information(request.session, user, daphne_version)
        #
        #     # --> Transfer current session
        #     userinfo.user = user
        #     userinfo.session = None
        #     userinfo.save()

        return userinfo


class Login(APIView):
    """
    Login a user
    """
    def post(self, request, format=None):

        # --> Authenticate user from request
        username = request.data['username']
        password = request.data['password']
        daphne_version = request.data['daphneVersion']
        user = authenticate(request, username=username, password=password)

        if user is not None:

            # # Try to look for user session object. If it exists, then the session will be changed to that. If not,
            # # the current session information will be transferred to the user
            # userinfo = self.handle_user_session(user, request, daphne_version)
            #
            # # Log the user in
            # login(request, user)
            #
            # # Get user private key
            # user_pk = get_user_pk(username)
            #
            # # Return the login response
            # return Response({
            #     'status': 'logged_in',
            #     'username': username,
            #     'pk': user_pk,
            #     'is_experiment_user': userinfo.is_experiment_user,
            #     'permissions': []
            # })

            return Response({
                'status': 'logged_in',
                'username': 'gapaza',
                'pk': '1',
            })
        else:
            return Response({
                'status': 'auth_error',
                'login_error': 'Invalid Login!'
            })


    def handle_user_session(self, user, request, daphne_version):
        userinfo = None

        # # --> 1. Check if UserInformation already exists
        # query = UserInformation.objects.filter(user__exact=user)
        # if len(query) > 0:
        #     # --> If UserInformation exists (return first)
        #     userinfo = query.first()
        #     userinfo.daphne_version = daphne_version
        #     userinfo.save()
        # else:
        #     # --> If UserInformation DNE (create UserInformation)
        #     userinfo = get_or_create_user_information(request.session, user, daphne_version)
        #
        #     # --> Transfer current session
        #     userinfo.user = user
        #     userinfo.session = None
        #     userinfo.save()

        return userinfo


class Logout(APIView):
    """
    Logout a user -> Important!! When the frontend logs out it needs to start fresh
    """
    def post(self, request, format=None):

        # Log the user out
        logout(request)
        # Return the logout response
        return Response({
            'message': 'User logged out.'
        })
