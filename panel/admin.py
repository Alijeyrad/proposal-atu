from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter
# you need import this for adding jalali calander widget
import django_jalali.admin as jadmin

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_filter = (
        ('date_added', JDateFieldListFilter),
    )

    empty_value_display = '-empty-'
    readonly_fields = ('date_added', 'date_edited')

    date_hierarchy = 'date_added'
    list_display = ('name', 'owner', 'prof_rahnama', 'status', )
    ordering = ['-date_added']
    search_fields = ['owner', 'name', 'prof_rahnama', ]
    list_filter = ('status', 'extention')