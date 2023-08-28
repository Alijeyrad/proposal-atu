from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter
# you need import this for adding jalali calander widget
import django_jalali.admin as jadmin

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = (
        ('date_joined', JDateFieldListFilter),
    )
    
    empty_value_display = '-empty-'

    # show jalali date in list display 
    list_display = ['email', 'first_name', 'last_name']
    date_hierarchy = 'date_joined'
    ordering = ['-date_joined']
    search_fields = ['first_name', 'last_name']
