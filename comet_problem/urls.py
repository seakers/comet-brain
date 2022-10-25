from django.urls import path
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path('load-problem', views.LoadProblem.as_view(), name='load-problem'),


]




urlpatterns = format_suffix_patterns(urlpatterns)