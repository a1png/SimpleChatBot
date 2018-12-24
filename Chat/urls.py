from django.conf.urls import url

from . import consumer
from . import views

websocket_urlpatterns = [
    url(r'^chat/$', consumer.ChatConsumer),
]

urlpatterns = [
    url(r'chatpage/$', views.chat, name='chat'),
]