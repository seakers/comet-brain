from django.urls import path
from comet_ws.consumers import CometConsumer


ws_routes = []
ws_routes.append(path('api/ws', CometConsumer.as_asgi()))