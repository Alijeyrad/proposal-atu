from django import template
from django.db.models import Q
from chat.models import Message

register = template.Library()

@register.inclusion_tag('messages/templatetags/message_notif.html')
def show_notif(user):
    if not user.is_authenticated:
        return {'should_show': False}
    
    unread_count = Message.objects.filter(
        Q(receiver = user) & Q(is_read = False)
    ).count()

    should_show = False if unread_count == 0 else True

    return {'should_show': should_show}