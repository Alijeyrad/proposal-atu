from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.contrib import messages as message_framework
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from core.settings import BASE_DIR
import os
from django.contrib.auth import get_user_model
from .models import Message
from .forms import MessageForm, ChatForm

# Create your views here.

User = get_user_model()

def messages(request):
    related_messages = Message.objects.all().filter(
        Q(sender__id=request.user.id) | Q(receiver__id=request.user.id)
    ).order_by('-date_sent')

    couples_set = set()
    for m in related_messages:
        if m.sender != m.receiver:
            couple = (m.sender, m.receiver)

            couples_set.add(couple)
            
    
    couples_list = list()
    for c in couples_set:
        sender = c[0]
        receiver = c[1]
        last_message = Message.objects.all().filter(
            (Q(sender__id__in = [sender.id, receiver.id]) & Q(receiver__id__in = [sender.id, receiver.id])) 
        ).order_by('-date_sent').first()

        if sender.id == request.user.id:
            mokhatab = receiver
        else:
            mokhatab = sender

        couples_list.append({
            'mokhatab': mokhatab,
            'sender': sender,
            'receiver': receiver,
            'last_message': last_message,
        })


        couples_list.sort(key=lambda x: x['last_message'].date_sent, reverse=True)

    couples_list_copy = list(couples_list)
    for item in couples_list:
        if item['sender'] != item['last_message'].sender:
            couples_list_copy.remove(item)


    if request.user.is_student:
        return render(request, 'messages/student-messages.html', {
            'messages_obj': couples_list_copy,
        })
    else:
        return render(request, 'messages/prof-messages.html', {
            'messages_obj': couples_list_copy,
        })



def chat(request, sender_id, receiver_id):
    if request.user.id not in [sender_id, receiver_id]:
        message_framework.error(request, 'به این صفحه دسترسی ندارید.')
        return HttpResponseRedirect(reverse('chat:chat', args=[request.user.id, sender_id]))


    participants = [sender_id, receiver_id]
    messages_obj = Message.objects.all().filter(
        Q(sender__id__in = participants) & Q(receiver__id__in = participants)
    ).exclude(
        sender__id = F('receiver__id')
    ).order_by('date_sent')

    last_message = messages_obj.last()

    if request.user != last_message.sender:
        save_messages = messages_obj.update(is_read = True)

    # check to see who is the message sender
    # and send their id to the template
    message_sender = ''
    if request.user.id == sender_id:
        message_sender = User.objects.get(id=receiver_id)
    else:
        message_sender = User.objects.get(id=sender_id)

    # get the form
    form = ChatForm()

    if request.user.is_student:
        return render(request, 'messages/student-chat.html', {
            'messages_obj': messages_obj,
            'message_sender': message_sender,
            'form': form,
        })
    else:
        return render(request, 'messages/prof-chat.html', {
            'messages_obj': messages_obj,
            'message_sender': message_sender,
            'form': form,
        })



def send_message(request, receiver_id=None):
    if request.method == 'POST':

        # this is when request is coming from
        # chat page => then a reciever_id is sent
        if receiver_id is not None:
            receiver = User.objects.get(id=receiver_id)
            form = ChatForm(request.POST, request.FILES)
            if form.is_valid():
                chat_obj = Message()
                chat_obj.receiver = receiver
                chat_obj.sender = request.user
                if request.FILES.get('chat_file', False):
                    name = request.FILES.get('chat_file')
                    file_name, file_extention = os.path.splitext(str(name))
                    chat_obj.chat_file = request.FILES['chat_file']
                    chat_obj.has_file = True
                    chat_obj.file_name = file_name
                    chat_obj.file_extention = file_extention
                chat_obj.content = form.cleaned_data['content']
                
                chat_obj.save()
                message_framework.success(request, 'پیام شما با موفقیت ارسال شد.')
                return HttpResponseRedirect(reverse('chat:chat', args=[request.user.id, receiver_id]))
            else:
                message_framework.error(request, 'مشکلی به وجود آمد. دوباره تلاش کنید.')
                return HttpResponseRedirect(reverse('chat:chat', args=[request.user.id, receiver_id]))
                

        # this is when request is coming from
        # new_message page
        else:
            form = MessageForm(request.POST, request.FILES)
            receiver = ""
            if form.is_valid():
                if request.user == form.cleaned_data['receiver']:
                    message_framework.warning(request, 'نمی‌توانید برای خودتان پیام ارسال کنید.')
                    return HttpResponseRedirect(reverse('dashboard:send_message'))
                
                if not form.cleaned_data['receiver']:
                    message_framework.warning(request, 'دریافت کننده پیام را انتخاب کنید.')
                    return HttpResponseRedirect(reverse('dashboard:send_message'))

                if request.FILES.get('chat_file', False):
                    message_obj = Message(chat_file=request.FILES['chat_file'])
                    message_obj.is_file = True
                    message_obj.sender = request.user
                    message_obj.receiver = form.cleaned_data['receiver']
                    if form.cleaned_data['content']:
                        message_obj.content = form.cleaned_data['content']
                else:
                    message_obj = Message()
                    message_obj.sender = request.user
                    message_obj.receiver = form.cleaned_data['receiver']
                    message_obj.content = form.cleaned_data['content']

                receiver = message_obj.receiver.id
                message_obj.save()

                message_framework.success(request, 'پیام شما با موفقیت ارسال شد.')
                return HttpResponseRedirect(reverse('chat:chat', args=[request.user.id, receiver]))
            else:
                message_framework.error(request, 'مشکلی به وجود آمد. دوباره تلاش کنید.')
                return HttpResponseRedirect(reverse('chat:messages'))

    if request.method == 'GET':
        if request.user.is_student:
            form = MessageForm()
            return render(request, 'messages/student-send-messages.html', {'form': form})
        else:
            form = MessageForm()
            return render(request, 'messages/prof-send-messages.html', {'form': form})
