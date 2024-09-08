from django.urls import path
from .consumers import FileTrackerConsumer

websocket_urlpatterns = [
    path('ws/file_tracker/', FileTrackerConsumer.as_asgi()),
]
