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

class MessagesView(View):
    def get(self, request):
        # Get related messages, ordered by date_sent
        related_messages = Message.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).order_by('-date_sent').select_related('sender', 'receiver')

        couples = {}
        prof_count = 0

        for message in related_messages:
            if message.sender != message.receiver:
                # Define a unique key for each conversation
                conversation_key = tuple(sorted((message.sender.id, message.receiver.id)))

                if conversation_key not in couples:
                    couples[conversation_key] = {
                        'mokhatab': message.receiver if message.sender == request.user else message.sender,
                        'sender': message.sender,
                        'receiver': message.receiver,
                        'last_message': message,
                    }

                    if couples[conversation_key]['mokhatab'].is_prof:
                        prof_count += 1

        # Sort conversations by the date of the last message
        sorted_couples = sorted(couples.values(), key=lambda x: x['last_message'].date_sent, reverse=True)

        template = 'messages/student-messages.html' if request.user.is_student else 'messages/prof-messages.html'

        context = {
            'messages_obj': sorted_couples,
            'prof_count': prof_count,
        }

        return render(request, template, context)




class ChatView(View):
    def get(self, request, sender_id, receiver_id):
        if request.user.id not in [sender_id, receiver_id]:
            message_framework.error(request, 'به این صفحه دسترسی ندارید.')
            return HttpResponseRedirect(reverse('chat:chat', args=[request.user.id, sender_id]))

        # Get the conversation messages, ordered by date_sent
        participants = [sender_id, receiver_id]
        messages_obj = Message.objects.filter(
            Q(sender__id__in=participants) & Q(receiver__id__in=participants)
        ).exclude(sender=F('receiver')).order_by('date_sent')

        # Update unread status for the last message
        last_message = messages_obj.last()
        if last_message and request.user != last_message.sender:
            messages_obj.update(is_read=True)

        # Determine the message sender
        message_sender_id = receiver_id if request.user.id == sender_id else sender_id
        message_sender = User.objects.get(id=message_sender_id)

        # Prepare the form
        form = ChatForm()

        # Choose the template based on user type
        template = 'messages/student-chat.html' if request.user.is_student else 'messages/prof-chat.html'

        context = {
            'messages_obj': messages_obj,
            'message_sender': message_sender,
            'form': form,
        }

        return render(request, template, context)



class SendMessageView(View):
    def post(self, request, receiver_id=None):
        """
            if request is coming from new_message => then a reciever_id is sent through the form
            (messages/student-send-messages.html or messages/prof-send-messages.html) page

            this is when request is coming from chat page => then a reciever_id is sent in the request
            (messages/student-chat.html or messages/prof-chat.html) 
        """

        if receiver_id is not None:
            form = ChatForm(request.POST, request.FILES)
        else:
            form = MessageForm(request.POST, request.FILES)
        
        if form.is_valid():
            message_obj = Message()
            message_obj.sender = request.user
            
            if receiver_id is not None:
                receiver = User.objects.get(id=receiver_id)
                message_obj.receiver = receiver
                message_obj.content = form.cleaned_data['content']
                
                if request.FILES.get('chat_file', False):
                    name = request.FILES.get('chat_file')
                    file_name, file_extention = os.path.splitext(str(name))
                    message_obj.chat_file = request.FILES['chat_file']
                    message_obj.has_file = True
                    message_obj.file_name = file_name
                    message_obj.file_extension = file_extention
            else:
                message_obj.receiver = form.cleaned_data['receiver']
                if request.FILES.get('chat_file', False):
                    message_obj.chat_file = request.FILES['chat_file']
                    message_obj.has_file = True
                message_obj.content = form.cleaned_data['content']
                
                if request.user == form.cleaned_data['receiver']:
                    message_framework.warning(request, 'نمی‌توانید برای خودتان پیام ارسال کنید.')
                    return HttpResponseRedirect(reverse('chat:send_new_message'))
                
                if not form.cleaned_data['receiver']:
                    message_framework.warning(request, 'دریافت کننده پیام را انتخاب کنید.')
                    return HttpResponseRedirect(reverse('chat:send_new_message'))

            message_obj.save()
            message_framework.success(request, 'پیام شما با موفقیت ارسال شد.')
            return HttpResponseRedirect(reverse('chat:chat', args=[request.user.id, message_obj.receiver.id]))
        else:
            message_framework.error(request, 'مشکلی به وجود آمد. دوباره تلاش کنید.')
            if receiver_id is not None:
                return HttpResponseRedirect(reverse('chat:chat', args=[request.user.id, receiver_id]))
            return HttpResponseRedirect(reverse('chat:messages'))
    
    def get(self, request):
        form = MessageForm()
        template = 'messages/student-send-messages.html' if request.user.is_student else 'messages/prof-send-messages.html'
        return render(request, template, {'form': form})
