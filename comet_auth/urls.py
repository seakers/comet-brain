from django.urls import path
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('register', views.Register.as_view(), name='register'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),

    path('check-status', views.CheckStatus.as_view(), name='check-status'),
    path('generate-session', views.GenerateSession.as_view(), name='generate-session'),
    path('get-user-pk', views.GetUserPk.as_view(), name='get-user-pk'),
    #
    # # --> Deprecated
    # path('reset-password', views.ResetPassword.as_view(), name='reset-password'),
    # path('confirm-guest', views.ConfirmGuest.as_view(), name='confirm-guest'),
]

urlpatterns = format_suffix_patterns(urlpatterns)