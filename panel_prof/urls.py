from django.urls import path
from . import views

app_name = 'panel_prof'

urlpatterns = [
    path('info', views.ProposalInfoProfView.as_view(), name='proposal_info'),
    path('proposal-accept', views.proposal_accept, name='proposal_accept'),
    path('proposal-assessment', views.proposal_assessment, name='proposal_assessment'),
    path('dissertation-judgment', views.dissertation_judgment, name='dissertation_judgment'),
    path('accept-request', views.accept_request, name='accept_request'),
]