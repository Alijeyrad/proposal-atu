from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    path('info', views.ProposalInfoView.as_view(), name='proposal_info'),
    path('download_file/<int:id>/<str:fileName>', views.download_file, name='download_file'),
    path('accept-request', views.ProposalAcceptRequestView.as_view(), name='proposal_accept_request'),
    path('dissertation-info', views.DissertationInfoView.as_view(), name='dissertation_info'),
    path('defa-request', views.defa_request, name='defa_request'),
]