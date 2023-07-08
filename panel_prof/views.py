from django.shortcuts import render

# Professor panel views


def proposal_info(request):
    return render(request, 'panel-prof/proposal-info.html')



def proposal_accept(request):
    return render(request, 'panel-prof/proposal-accept.html')



def proposal_assessment(request):
    return render(request, 'panel-prof/proposal-assessment.html')



def dissertation_judgment(request):
    return render(request, 'panel-prof/dissertation-judgment.html')



def prof_messages(request):
    return render(request, 'panel-prof/prof_messages.html')



def prof_chat(request):
    return render(request, 'panel-prof/prof-chat.html')



def accept_request(request):
    return render(request, 'panel-prof/accept-request.html')