import os
from django.shortcuts import render
from django.views import View
from .forms import ProposalForm
from .models import Proposal
from django.shortcuts import redirect

# Student panel views


class ProposalInfoView(View):
    template_name = 'panel-student/proposal-info.html'

    def get(self, request, *args, **kwargs):
        proposal = Proposal.objects.filter(owner=request.user.id).first()
        form = ProposalForm(instance=proposal)
        return render(request, self.template_name, {'form': form, 'proposal': proposal})

    def post(self, request, *args, **kwargs):
        proposal = Proposal.objects.filter(owner=request.user.id).first()
        form = ProposalForm(request.POST, request.FILES, instance=proposal)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.owner = request.user
            name = request.FILES['file']
            file_name, file_extention = os.path.splitext(str(name))
            proposal.name = file_name
            proposal.extention = file_extention[1:]
            proposal.save()
            return redirect('panel:proposal_info')  # Redirect back to the same page
        return render(request, self.template_name, {'form': form})



def proposal_accept_request(request):
    return render(request, 'panel-student/proposal-accept-request.html')



def dissertation_info(request):
    return render(request, 'panel-student/dissertation-info.html')



def defa_request(request):
    return render(request, 'panel-student/defa-request.html')



def student_messages(request):
    return render(request, 'panel-student/messages.html')


def student_chat(request):
    return render(request, 'panel-student/chat.html')