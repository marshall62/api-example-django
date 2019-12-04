from django import forms
from django.forms import widgets
import re

# Add your forms here
class CheckinForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    ssn4 = forms.CharField(max_length=4, label='Last 4 digits of SSN', required=False)

    def clean_ssn4 (self):
        ssn4 = self.cleaned_data['ssn4']
        if len(ssn4) > 0:
            ssn_valid = re.match("\d{4}$",ssn4)
            if not ssn_valid:
                raise forms.ValidationError("SSN must be 4 digits")
        return ssn4


class PatientInfoForm (forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    date_of_birth = forms.DateField(required=False)
    gender = forms.CharField()
    address = forms.CharField(required=False)
    recent_changes = forms.CharField(widget=forms.Textarea,
                                     label='Describe any recent changes to your health',
                                     required=False)