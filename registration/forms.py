from django import forms
from .models import *
from .choices import *
from django_countries.widgets import CountrySelectWidget

class MemberForm(forms.ModelForm):
    '''form for Attendee model'''
    
    class Meta:
        model = Member
        fields = [
            'name',
            'sirname',
            #'sex',
            'street',
            'streetnumber',
            'postcode',
            'location',
            'country',
            'email',
            'phonenumber',
            'birthdate',
            'entrydate',
            'fee',
            'iban',
            'bic',
            'bankname',
            'memberstatus',
            ]
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Vorname'}),
            'sirname': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Nachname'}),
            #'sex': forms.Select(attrs={'class':'form-control'}),
            'street': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Straße'}),
            'streetnumber': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Hausnummer'}),
            'postcode': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Postleitzahl'}),
            'location': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Ort'}),
            'country': CountrySelectWidget(attrs={'class':'form-control input-sm', 'placeholder':'Land'}),
            'email': forms.EmailInput(attrs={'class':'form-control input-sm', 'placeholder':'Emailadresse'}),
            'phonenumber': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Telefonnummer'}),
            'birthdate': forms.DateInput(attrs={'class':'form-control input-sm', 'placeholder':'Geburtstag'}),
            'entrydate': forms.DateInput(attrs={'class':'form-control input-sm', 'placeholder':'Eintrittsdatum'}),
            'fee': forms.RadioSelect(attrs={}, choices=FEE),
            'iban': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'IBAN'}),
            'bic': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'BIC'}),
            'bankname': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Kreditinstitut'}),
            'memberstatus': forms.RadioSelect(attrs={'class':'memberstatus'}),
        }
        
class AgreementForm(forms.ModelForm):
    
    class Meta:
        model = Member
        fields = [
            'sepa_agree',
            'rules_agree',
            'privacy_agree',
            ]
        widgets = {
            'sepa_agree': forms.CheckboxInput(attrs={}),
            'rules_agree': forms.CheckboxInput(attrs={}),
            'privacy_agree': forms.CheckboxInput(attrs={}),
        }
    
