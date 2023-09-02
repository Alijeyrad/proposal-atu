from django.urls import path
from . import views

app_name = 'panel_prof'

urlpatterns = [
    path('info', views.ProposalInfoProfView.as_view(), name='proposal_info'),
    path('proposal-accept', views.ProposalAcceptView.as_view(), name='proposal_accept'),
    path('accept-request', views.AcceptRequest.as_view(), name='accept_request'),
    path('proposal-assessment', views.proposal_assessment, name='proposal_assessment'),
    path('dissertation-judgment', views.dissertation_judgment, name='dissertation_judgment'),
]