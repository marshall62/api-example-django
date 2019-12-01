from django import forms
from django.forms import widgets


# Add your forms here
class CheckinForm(forms.Form):
    fname = forms.CharField()
    lname = forms.CharField()
    ssn4 = forms.CharField(max_length=4)


class PatientInfoForm (forms.Form):
    fname = forms.CharField()
    lname = forms.CharField()