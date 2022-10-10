from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.sessions.models import Session

from comet_auth.models import UserInformation




def get_or_create_user_information(session, user):
    userinfo = get_user_information(session, user)
    if userinfo is not None:
        return userinfo
    if user.is_authenticated:
        return create_user_information(username=user.username)
    else:
        return create_user_information(session_key=session.session_key)


def get_user_information(session, user):

    if user.is_authenticated:
        # First try lookup by username
        userinfo_qs = UserInformation.objects.filter(user__exact=user).select_related("user")
    else:
        # Try to look by session key
        # If no session exists, create one here
        if session.session_key is None:
            session.create()
        q_session = get_session(session.session_key)
        if q_session is None:
            return None
        else:
            userinfo_qs = UserInformation.objects.filter(session_id__exact=q_session.session_key).select_related("user")

    if len(userinfo_qs) >= 1:
        user_info = userinfo_qs[0]
        return user_info
    elif len(userinfo_qs) == 0:
        return None


def get_session(session_key):
    session_objs = Session.objects.filter(session_key=session_key)
    if len(session_objs) == 0:
        return None
    else:
        return session_objs[0]

def create_user_information(session_key=None, username=None):
    assert session_key is not None or username is not None

    with transaction.atomic():
        # --> 1. UserInformation
        if username is not None and session_key is None:
            user_info = UserInformation(user=User.objects.get(username=username))
        elif session_key is not None and username is None:
            q_session = get_session(session_key)
            if q_session is None:
                return None
            user_info = UserInformation(session=q_session)
        else:
            raise Exception("Unexpected input for create_user_information")

        user_info.save()

        return user_info




