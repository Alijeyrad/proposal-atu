from django import forms
from panel.models import Proposal
from django.contrib.auth import get_user_model


User = get_user_model()

class MyModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class ProposalActionForm(forms.Form):
    proposal_id = forms.IntegerField()
    action = forms.ChoiceField(choices=[('accept-rahnama', 'Accept Rahnama'), ('accept-moshaver', 'Accept Moshaver'), ('reject', 'Reject')])

    def clean(self):
        cleaned_data = super().clean()
        proposal_id = cleaned_data.get('proposal_id')
        action = cleaned_data.get('action')

        if not Proposal.objects.filter(pk=proposal_id).exists():
            raise forms.ValidationError("Invalid proposal ID.")

        return cleaned_data


class ProposalAdminForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['profs_arzyab']

    profs = User.objects.filter(is_prof=True)

    profs_arzyab = MyModelMultipleChoiceField(
        queryset=profs,
    )
