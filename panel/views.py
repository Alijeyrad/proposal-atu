from django.shortcuts import render

# Create your views here.


def proposal_info(request):
    return render(request, 'panel-student/proposal-info.html')



def proposal_accept_request(request):
    return render(request, 'panel-student/proposal-accept-request-info.html')



def dissertation_info(request):
    return render(request, 'panel-student/dissertation-info.html')



def defa_request(request):
    return render(request, 'panel-student/defa-request.html')



def student_messages(request):
    return render(request, 'panel-student/student-messages.html')


def student_chat(request):
    return render(request, 'panel-student/student-chat.html')