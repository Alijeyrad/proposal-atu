from django.shortcuts import render
from django.views import View
from django.db.models import Q, F
from panel.models import Proposal

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




class ProposalAcceptProfView(View):
    template_name = 'panel-prof/proposal-accept.html'

    def get(self, request, *args, **kwargs):
        proposal_id = kwargs.get('id', False)
        action = kwargs.get('action', False)
        
        if proposal_id:
            proposal = Proposal.objects.get(pk=proposal_id)

            if action == "accept-rahnama":
                proposal.status = Proposal.WF_MOSHAVER_CONFIRM
                proposal.rahnama_one_accepted = True
                proposal.save()
                # message framework
            
            elif action == "accept-moshaver":
                proposal.status = Proposal.WF_ARZYAB_ASIGNMENT
                proposal.moshaver_one_accepted = True
                proposal.save()
                # message framework

            elif action == "reject":
                # redirect to chat page
                # message framework
                h=1

        # Get proposals where the professor is either prof_rahnama or prof_moshaver
        rahnama_proposals = Proposal.objects.filter(
            Q(prof_rahnama=request.user) and Q(status=Proposal.WF_RAHNAMA_CONFIRM)
        )

        moshaver_proposals = Proposal.objects.filter(
            Q(prof_moshaver=request.user) and Q(status=Proposal.WF_MOSHAVER_CONFIRM)
        )

        context = {
            'rahnama_proposals': rahnama_proposals,
            'moshaver_proposals': moshaver_proposals,
        }
        return render(request, self.template_name, context)




def proposal_assessment(request):
    return render(request, 'panel-prof/proposal-assessment.html')



def dissertation_judgment(request):
    return render(request, 'panel-prof/dissertation-judgment.html')



def accept_request(request):
    return render(request, 'panel-prof/accept-request.html')