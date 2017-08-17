#coding:utf8
from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from localflavor.generic.checksums import luhn
from localflavor.generic.checksums import ean
from localflavor.generic.checksums import ean
import ast
import datetime
from .models import *
from .forms import *


##  TODO:
##  - check if address data is valid
##  - PDF download of registration data with AGBs, ...
##  - improve design
##  - improve email text


## mail to send message if someone signed up
MAIL = 'vorstand@eigenbaukombinat.de'

## mail address shown as sender for mail
SENDER_MAIL = 'vorstand@eigenbaukombinat.de'

def register(request):
    '''First register page to input personal data'''
    
    if request.method == 'POST':
        memberform = MemberForm(request.POST)
        if memberform.is_valid():
            name = memberform.cleaned_data['name']
            surname = memberform.cleaned_data['surname']
            street = memberform.cleaned_data['street']
            streetnumber = memberform.cleaned_data['streetnumber']
            postcode = memberform.cleaned_data['postcode']
            location = memberform.cleaned_data['location']
            country = memberform.cleaned_data['country']
            email = memberform.cleaned_data['email']
            phonenumber = memberform.cleaned_data['phonenumber']
            birthdate = memberform.cleaned_data['birthdate']
            fee = memberform.cleaned_data['fee']
            memberstatus = memberform.cleaned_data['memberstatus']
            #encapsulate to preview on next page
            preview_data = {
                'name':name,
                'surname':surname,
                'street':street,
                'streetnumber':streetnumber,
                'postcode':postcode,
                'location':location,
                'country':country,
                'email':email,
                'phonenumber':phonenumber,
                'birthdate':birthdate,
                'fee': '%.2f' % fee,
                'memberstatus':memberstatus,
            }
            form = AgreementForm()
            return render(request, 'register_preview.html', {'preview_data':preview_data, 'form':form, 'memberform':memberform})
    
    form = MemberForm()
    feeform = FeeForm()
    return render(request, 'register_page.html', {'form':form, 'feeform':feeform})
    
def preview(request):
    '''Second register page. Show a preview of inputed data and to accept rules'''
    
    
    if request.method == 'POST':
        form = AgreementForm(request.POST)
        memberform = MemberForm(request.POST)
        if form.is_valid() and memberform.is_valid():
            #check if rules are accepted if not show message
            if form.cleaned_data['sepa_agree'] == True and \
                form.cleaned_data['rules_agree'] == True and \
                form.cleaned_data['privacy_agree'] == True and \
                form.cleaned_data['iban']:

                #check if member with this name already exists if not proceed
                if Member.objects.filter(
                                            name=memberform.cleaned_data['name'], 
                                            surname=memberform.cleaned_data['surname'], 
                                            email=memberform.cleaned_data['email']
                                        ).exists() == False:
                                            
                    member = Member()
                    member.name = memberform.cleaned_data['name']
                    member.surname = memberform.cleaned_data['surname']
                    member.street = memberform.cleaned_data['street']
                    member.streetnumber = memberform.cleaned_data['streetnumber']
                    member.postcode = memberform.cleaned_data['postcode']
                    member.location = memberform.cleaned_data['location']
                    member.country = memberform.cleaned_data['country']
                    member.email = memberform.cleaned_data['email']
                    member.phonenumber = memberform.cleaned_data['phonenumber']
                    member.birthdate = memberform.cleaned_data['birthdate']
                    member.fee = memberform.cleaned_data['fee']
                    member.memberstatus = memberform.cleaned_data['memberstatus']
                    member.status = 'pending'
                    member.iban = form.cleaned_data['iban']
                    member.sepa_agree = form.cleaned_data['sepa_agree']
                    member.rules_agree = form.cleaned_data['rules_agree']
                    member.privacy_agree = form.cleaned_data['privacy_agree']
                    member.save()
                                    
                  #  try:
                  #      send_mail(
                  #          'Eigenbaukombinat Online Registrierung',
                  #          'Deine Registrierung für das Eigenbaukombinat ist erfolgreich eingegangen. Bitte habe noch etwas Geduld bis diese bestätigt wurde.',
                  #          SENDER_MAIL,
                  #          [member.email],
                  #          fail_silently=False,
                  #          )
                  #      send_mail(
                  #          'Eigenbaukombinat Online Registrierung',
                  #          'Ein neues Mitglied hat sich registriert',
                  #          SENDER_MAIL,
                  #          [MAIL],
                  #          fail_silently=False,
                  #          )
                  #  except:
                  #      return render(request, 'register_status.html',{'status':'notsend'})
                    
                    return render(request, 'register_status.html',{'status':'success'})
                else:
                    return render(request, 'register_status.html', {'status':'registered'})
            else:
                return render(request, 'register_preview.html', {'form':form, 'memberform':memberform, 'status':'failed'})
    
    form = AgreementForm()
    return render(request, 'register_preview.html', {'form':form})
