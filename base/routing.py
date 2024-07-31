from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/image_generation/', consumers.ImageGenerationConsumer.as_asgi()),
]