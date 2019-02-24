#coding:utf8
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
            'surname',
            'street',
            'streetnumber',
            'postcode',
            'location',
            'country',
            'email',
            'phonenumber',
            'birthdate',
            'fee',
            'memberstatus',
            ]
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Vorname'}),
            'surname': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Nachname'}),
            'street': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Straße'}),
            'streetnumber': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Hausnummer'}),
            'postcode': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Postleitzahl'}),
            'location': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Ort'}),
            'country': CountrySelectWidget(attrs={'class':'form-control input-sm', 'placeholder':'Land'}),
            'email': forms.EmailInput(attrs={'class':'form-control input-sm', 'placeholder':'Emailadresse'}),
            'phonenumber': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Telefonnummer'}),
            'birthdate': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Geburtstag'}),
            'fee': forms.NumberInput(attrs={'value':'12'}),
            'memberstatus': forms.RadioSelect(attrs={'class':'memberstatus'}),
        }
    def clean(self):
        data = self.cleaned_data
        if data['fee'] < 0:
            raise forms.ValidationError('Nich bescheissen!!11elf') 
        if data['memberstatus'] == 'member' and data['fee'] < 18:
            raise forms.ValidationError('Nich bescheissen!!11elf') 

class AgreementForm(forms.ModelForm):
    
    class Meta:
        model = Member
        fields = [
            'sepa_agree',
            'rules_agree',
            'privacy_agree',
            'iban',

            ]
        widgets = {
            'sepa_agree': forms.CheckboxInput(attrs={}),
            'rules_agree': forms.CheckboxInput(attrs={}),
            'privacy_agree': forms.CheckboxInput(attrs={}),
            'iban': forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Bitte hier die IBAN ihres Kontos eingeben von der die Beiträge abgebucht werden sollen.', 'data-validation':'iban'}),

        }

class FeeForm(forms.ModelForm):
        
        class Meta:
            model = Member
            fields = [
                'fee',
                ]
            widgets = {
                'fee': forms.RadioSelect(attrs={}, choices=FEE),
            }
