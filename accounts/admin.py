from django.contrib import admin
from .models import User, Profile, StudyField, Department
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

    list_display = ['email', 'first_name', 'last_name']
    date_hierarchy = 'date_joined'
    ordering = ['-date_joined']
    search_fields = ['first_name', 'last_name']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'

    list_display = ['maghta', 'study_field', 'student_number']
    search_fields = ['student_number', 'study_field']

@admin.register(StudyField)
class StudyFieldAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'

    list_display = ['title', 'sub_title', 'department']
    search_fields = ['title', 'sub_title', 'department']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'

    list_display = ['title']
