from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    path('info', views.proposal_info, name='index'),
]