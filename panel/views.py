import os
from django.shortcuts import render
from django.views import View
from .forms import ProposalFormFile, ProposalFormProf, ProposalFormAccept
from .models import Proposal
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.contrib import messages as message_framework
from django.contrib.auth.decorators import login_required, user_passes_test 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from core.settings import BASE_DIR
import mimetypes
import os

# Student panel views


class ProposalInfoView(View):
    template_name = 'panel-student/proposal-info.html'

    def get(self, request, *args, **kwargs):
        proposal = Proposal.objects.filter(owner=request.user.id).first()
        formFile = ProposalFormFile(instance=proposal)
        formProf = ProposalFormProf(instance=proposal)
        return render(request, self.template_name, {
            'formFile': formFile,
            'formProf': formProf,
            'proposal': proposal
        })

    def post(self, request, *args, **kwargs):
        proposal = Proposal.objects.filter(owner=request.user.id).first()
        form_type = request.POST.get('form_type')
        
        if form_type == 'file_only':
            form = ProposalFormFile(request.POST, request.FILES, instance=proposal)
            if form.is_valid():
                proposal = form.save(commit=False)
                proposal.owner = request.user
                name = request.FILES['file']
                file_name, file_extention = os.path.splitext(str(name))
                proposal.name = file_name
                proposal.extention = file_extention[1:]
                proposal.save()
                return redirect('panel:proposal_info')  # Redirect back to the same page
        else:
            form = ProposalFormProf(request.POST, instance=proposal)
            if form.is_valid():
                form.save()
                return redirect('panel:proposal_info')
        

        return render(request, self.template_name, {'form': form})



class ProposalAcceptRequestView(View):
    template_name = 'panel-student/proposal-accept-request.html'

    def get(self, request, *args, **kwargs):
        proposal = Proposal.objects.filter(owner=request.user.id).first()
        formFile = ProposalFormFile(instance=proposal)
        formAccept = ProposalFormAccept(instance=proposal)
        return render(request, self.template_name, {
            'formFile': formFile,
            'formAccept': formAccept,
            'proposal': proposal
        })

    def post(self, request, *args, **kwargs):
        proposal = Proposal.objects.filter(owner=request.user.id).first()
        form_type = request.POST.get('form_type')
        
        if form_type == 'file_only':
            form = ProposalFormFile(request.POST, request.FILES, instance=proposal)
            if form.is_valid():
                proposal = form.save(commit=False)
                proposal.owner = request.user
                name = request.FILES['file']
                file_name, file_extention = os.path.splitext(str(name))
                proposal.name = file_name
                proposal.extention = file_extention[1:]
                proposal.save()
                return redirect('panel:proposal_accept_request')  # Redirect back to the same page
        else:
            form = ProposalFormAccept(request.POST, request.FILES, instance=proposal)
            if form.is_valid():
                proposal.status = Proposal.REQEUST_SENT_2
                form.save()
                # send confirm message
                return redirect('panel:proposal_accept_request')
        

        formFile = ProposalFormFile(instance=proposal)
        formAccept = ProposalFormAccept(instance=proposal)
        return render(request, self.template_name, {
            'formFile': formFile,
            'formAccept': formAccept,
            'proposal': proposal
        })



def dissertation_info(request):
    return render(request, 'panel-student/dissertation-info.html')



def defa_request(request):
    return render(request, 'panel-student/defa-request.html')



def student_messages(request):
    return render(request, 'panel-student/messages.html')


def student_chat(request):
    return render(request, 'panel-student/chat.html')


def download_proposal(request, id):
    proposal = Proposal.objects.get(pk = id)
    file_name = proposal.name + '.' + proposal.extention
    file_path = proposal.file.path

    mime_type, _ = mimetypes.guess_type(file_path)
    fl = open(file_path, 'rb')
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % file_name

    return response


def download_file(request, id, fileName):
    proposal = Proposal.objects.get(pk = id)
    if fileName == "hamanand":
        file_name = proposal.hamanand_juii_file.name
        file_path = proposal.hamanand_juii_file.path

        mime_type, _ = mimetypes.guess_type(file_path)
        fl = open(file_path, 'rb')
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name

    if fileName == "irandoc":
        file_name = proposal.irandoc_file.name
        file_path = proposal.hamanand_juii_file.path

        mime_type, _ = mimetypes.guess_type(file_path)
        fl = open(file_path, 'rb')
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name

    return response