from django.urls import path
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path('run-data-mining', views.RunDataMining.as_view(), name='run-data-mining'),
]




urlpatterns = format_suffix_patterns(urlpatterns)