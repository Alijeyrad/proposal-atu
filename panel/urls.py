from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    path('info', views.ProposalInfoView.as_view(), name='proposal_info'),
    path('download_proposal/<int:id>', views.download_proposal, name='download_proposal'),
    path('download_dissertation/<int:id>', views.download_dissertation, name='download_dissertation'),
    path('download_file/<int:id>/<str:fileName>', views.download_file, name='download_file'),
    path('accept-request', views.ProposalAcceptRequestView.as_view(), name='proposal_accept_request'),
    path('dissertation-info', views.DissertationInfoView.as_view(), name='dissertation_info'),
    path('defa-request', views.defa_request, name='defa_request'),
    path('messages', views.student_messages, name='student_messages'),
    path('chat', views.student_chat, name='student_chat'),
]