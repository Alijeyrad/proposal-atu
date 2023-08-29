from django import forms
from .models import Proposal, Dissertation
from django.contrib.auth import get_user_model


User = get_user_model()

class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class ProposalFormFile(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['file']


class ProposalFormAccept(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['hamanand_juii_file', 'irandoc_file']
    

class ProposalFormProf(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['prof_rahnama', 'prof_moshaver']

    profs = User.objects.filter(is_prof=True)

    prof_rahnama = MyModelChoiceField(
        queryset = profs,
        empty_label = 'استاد راهنمای خود را انتخاب کنید',
        to_field_name = 'id'
    )
    
    prof_moshaver = MyModelChoiceField(
        queryset = profs,
        empty_label = 'استاد مشاور خود را انتخاب کنید',
        to_field_name = 'id'
    )


class DissertationFormFile(forms.ModelForm):
    class Meta:
        model = Dissertation
        fields = ['file']


class DissertationFormProf(forms.ModelForm):
    class Meta:
        model = Dissertation
        fields = ['prof_rahnama', 'prof_moshaver']

    profs = User.objects.filter(is_prof=True)

    prof_rahnama = MyModelChoiceField(
        queryset = profs,
        empty_label = 'استاد راهنمای خود را انتخاب کنید',
        to_field_name = 'id'
    )
    
    prof_moshaver = MyModelChoiceField(
        queryset = profs,
        empty_label = 'استاد مشاور خود را انتخاب کنید',
        to_field_name = 'id'
    )