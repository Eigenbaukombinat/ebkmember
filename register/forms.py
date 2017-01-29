from django import forms
from .models import *

class MemberTypeForm(forms.ModelForm):
    '''form for choosing the type of membership'''
    
    class Meta:
        model = MemberRegistration 
        fields = ['membertype',]
        widgets = {
            'membertype': forms.RadioSelect(),
        }
        

class NormalMemberForm(forms.ModelForm):
	"""Form for normal member form data"""

	class Meta:
		model = MemberRegistration
		fields = [
			'firstname',
			'lastname',
			'street',
			'postcode', 
			'country', 
			'email', 
			'birthdate',
			'entrydate', 
			'fee', 
			'customfee', 
			'iban', 
			'sepa_agree']

class CompanyMemberForm(forms.ModelForm):
	class Meta:
		model = MemberRegistration
		fields = [
		    'company',
			'firstname',
			'lastname',
			'street',
			'postcode', 
			'country', 
			'email', 
			'entrydate', 
			'fee', 
			'customfee', 
			'iban', 
			'sepa_agree']