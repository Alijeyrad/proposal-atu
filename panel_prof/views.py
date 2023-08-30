from django.shortcuts import render
from django.views import View
from django.db.models import Q, F
from panel.models import Proposal

# Professor panel views


class ProposalInfoProfView(View):
    template_name = 'panel-prof/proposal-info.html'
    
    def get(self, request, *args, **kwargs):
        current_professor = request.user
        proposals = Proposal.objects.all().filter(
                Q(prof_rahnama=request.user) | Q(profs_arzyab__id=request.user.id)
            ).order_by('-date_added')

        # Get proposals where the professor is either prof_rahnama or prof_moshaver
        # proposals = Proposal.objects.filter(prof_rahnama=current_professor) | Proposal.objects.filter(prof_moshaver=current_professor)

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



# return render(request, 'panel-prof/proposal-info.html')



def proposal_accept(request):
    return render(request, 'panel-prof/proposal-accept.html')



def proposal_assessment(request):
    return render(request, 'panel-prof/proposal-assessment.html')



def dissertation_judgment(request):
    return render(request, 'panel-prof/dissertation-judgment.html')



def accept_request(request):
    return render(request, 'panel-prof/accept-request.html')