from django import forms
from django.contrib.auth import get_user_model
from .models import Message


User = get_user_model()

class ChatForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'chat_file']

    content = forms.CharField(
        widget = forms.Textarea(
            attrs={
                'class': "chat-textarea-chatpage",
                'placeholder': "متن پیام",
            }
        )
    )

class MessageForm(ChatForm):
    class Meta:
        model = Message
        fields = ['content', 'chat_file', 'receiver']
        
    receivers = User.objects.all().filter(is_prof=True)
        
    receiver = forms.ModelChoiceField(
        queryset = receivers,
        empty_label = 'ارسال به ...',
        to_field_name= 'id'
    )