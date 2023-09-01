from django import forms
from panel.models import Proposal

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
