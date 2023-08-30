from django.contrib import admin
from .models import Message

# Register your models here.

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    readonly_fields = ('date_sent',)