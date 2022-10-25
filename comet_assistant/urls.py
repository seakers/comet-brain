from django.urls import path
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path('command', views.Command.as_view(), name='command'),


]




urlpatterns = format_suffix_patterns(urlpatterns)