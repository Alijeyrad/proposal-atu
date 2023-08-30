from django.urls import path
from .views import *

app_name = 'chat'

urlpatterns = [
    path('messages', messages, name='messages'),
    path('send_message', send_message, name='send_new_message'),
    path('send_message/<int:receiver_id>', send_message, name='send_message'),
    path('<int:sender_id>/<int:receiver_id>', chat, name='chat'),
]