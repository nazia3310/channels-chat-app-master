from django.urls import path
from app.consumers import ChatAsyncWebsocketConsumer

ws_urlpatterns = [
    path("ws/chat/<str:receiver>/", ChatAsyncWebsocketConsumer.as_asgi()),
]