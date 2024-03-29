from django.shortcuts import render
from django.views import View
from django.db.models import Q, F
from panel.models import Proposal
from .forms import ProposalActionForm, ProposalAdminForm
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages as message_framework

# Professor panel views

class ProposalInfoProfView(View):
    template_name = 'panel-prof/proposal-info.html'
    
    def get(self, request, *args, **kwargs):
        # Get proposals where the professor is either prof_rahnama or prof_moshaver
        rahnama_proposals = Proposal.objects.filter(
            Q(prof_rahnama=request.user)
        )

        moshaver_proposals = Proposal.objects.filter(
            Q(prof_moshaver=request.user)
        )
        
        context = {
            'rahnama_proposals': rahnama_proposals,
            'moshaver_proposals': moshaver_proposals,
        }
        return render(request, self.template_name, context)



class ProposalAcceptView(View):
    template_name = 'panel-prof/proposal-accept.html'

    def post(self, request, *args, **kwargs):
        form = ProposalActionForm(request.POST)
        
        if form.is_valid():
            proposal_id = form.cleaned_data['proposal_id']
            action = form.cleaned_data['action']
            proposal = Proposal.objects.get(pk=proposal_id)

            if action == "accept-rahnama":
                proposal.status = Proposal.WF_MOSHAVER_CONFIRM
                proposal.rahnama_one_accepted = True
                proposal.save()
                message_framework.success(request, 'ProposalAccepted rahnama')
            
            elif action == "accept-moshaver":
                proposal.status = Proposal.WF_ARZYAB_ASIGNMENT
                proposal.moshaver_one_accepted = True
                proposal.save()
                message_framework.success(request, 'ProposalAccepted moshaver')

            elif action == "reject":
                # Redirect to chat page
                message_framework.warning(request, 'ProposalRejected')
                return HttpResponseRedirect(reverse('chat:chat', args=[request.user.id, proposal.owner.id]))
        else:
            pass
            # Handle form errors here

        return HttpResponseRedirect(reverse('panel_prof:proposal_accept'))
    
    def get(self, request, *args, **kwargs):
        # Get proposals where the professor is either prof_rahnama or prof_moshaver
        moshaver_proposals = Proposal.objects.filter(
            Q(prof_moshaver=request.user), Q(status=Proposal.WF_MOSHAVER_CONFIRM)
        )
        rahnama_proposals = Proposal.objects.filter(
            Q(prof_rahnama=request.user), Q(status=Proposal.WF_RAHNAMA_CONFIRM)
        )


        print(moshaver_proposals)

        context = {
            'rahnama_proposals': rahnama_proposals,
            'moshaver_proposals': moshaver_proposals,
        }
        return render(request, self.template_name, context)



class AcceptRequest(View):
    template_name = 'panel-prof/accept-request.html'

    def post(self, request, *args, **kwargs):
        form = ProposalAdminForm(request.POST)
        
        if form.is_valid():
            proposal_id = form.cleaned_data['p_id']
            proposal = Proposal.objects.get(pk=proposal_id)
            
            # Update the proposal instance with the form data and save it
            form = ProposalAdminForm(request.POST, instance=proposal)
            proposal = form.save(commit=False)  # Save without committing to the database
            
            proposal.status = Proposal.WF_ARZYAB_CONFIRM
            proposal.save()  # Save the updated status
            message_framework.success(request, 'WF_ARZYAB_CONFIRM')
            return HttpResponseRedirect(reverse('panel_prof:accept_request'))
        else:
            message_framework.error(request, 'مشکل')
            return HttpResponseRedirect(reverse('panel_prof:accept_request'))

    def get(self, request, *args, **kwargs):
        # get all proposals waiting for arzyab asignment
        wf_arzyab_proposals = Proposal.objects.filter(
            Q(status=Proposal.WF_ARZYAB_ASIGNMENT)
        )

        # get all proposals waiting for final confirmation
        wf_admin_proposals = Proposal.objects.filter(
            Q(status=Proposal.WF_ADMIN_CONFIRM)
        )

        form = ProposalAdminForm()

        context = {
            'wf_arzyab_proposals': wf_arzyab_proposals,
            'wf_admin_proposals': wf_admin_proposals,
            'form': form
        }
        
        return render(request, self.template_name, context)



def proposal_assessment(request):
    return render(request, 'panel-prof/proposal-assessment.html')



def dissertation_judgment(request):
    return render(request, 'panel-prof/dissertation-judgment.html')

