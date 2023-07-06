from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    path('info', views.proposal_info, name='proposal_info'),
    path('accept-request', views.proposal_accept_request, name='proposal_accept_request'),
    path('dissertation-info', views.dissertation_info, name='dissertation_info'),
    path('defa-request', views.defa_request, name='defa_request'),
    path('messages', views.student_messages, name='student_messages'),
    path('chat', views.student_chat, name='student_chat'),
]