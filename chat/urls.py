from django.urls import path
from .views import *

app_name = 'chat'

urlpatterns = [
    path('messages', MessagesView.as_view(), name='messages'),
    path('send_message', SendMessageView.as_view(), name='send_new_message'),
    path('send_message/<int:receiver_id>', SendMessageView.as_view(), name='send_message'),
    path('<int:sender_id>/<int:receiver_id>', ChatView.as_view(), name='chat'),
]