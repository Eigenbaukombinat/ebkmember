from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
import ast
import datetime
from .models import *
from .forms import *


##  TODO:
##  - check if bank data is valid
##  - check if address data is valid
##  - PDF download of registration data with AGBs, ...
##  - improve design
##  - improve email text
##  - add countrylist


## mail to send message if someone signed up
MAIL = 'example@example.com'

## mail address shown as sender for mail
SENDER_MAIL = 'sender@example.com'

def register(request):
    '''First register page to input personal data'''
    
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            sirname = form.cleaned_data['sirname']
            street = form.cleaned_data['street']
            streetnumber = form.cleaned_data['streetnumber']
            postcode = form.cleaned_data['postcode']
            location = form.cleaned_data['location']
            country = form.cleaned_data['country']
            email = form.cleaned_data['email']
            phonenumber = form.cleaned_data['phonenumber']
            birthdate = form.cleaned_data['birthdate']
            birthdate = birthdate.strftime('%d/%m/%Y')   
            entrydate = form.cleaned_data['entrydate']
            entrydate = entrydate.strftime('%d/%m/%Y')
            fee = form.cleaned_data['fee']
            iban = form.cleaned_data['iban']
            bic = form.cleaned_data['bic']
            bankname = form.cleaned_data['bankname']
            memberstatus = form.cleaned_data['memberstatus']
            
            #encapsulate to preview on next page
            preview_data = {
                'name':name,
                'sirname':sirname,
                'street':street,
                'streetnumber':streetnumber,
                'postcode':postcode,
                'location':location,
                'country':country,
                'email':email,
                'phonenumber':phonenumber,
                'birthdate':birthdate,
                'entrydate':entrydate,
                'fee':fee,
                'iban':iban,
                'bic':bic,
                'bankname':bankname,
                'memberstatus':memberstatus,
            }
            form = AgreementForm()
            return render(request, 'register_preview.html', {'preview_data':preview_data, 'form':form})
    
    form = MemberForm()
    
    return render(request, 'register_page.html', {'form':form})
    
def preview(request):
    '''Second register page. Show a preview of inputed data and to accept rules'''
    
    
    if request.method == 'POST':
        form = AgreementForm(request.POST)
        preview_data = ast.literal_eval(request.POST['preview_data'])
        if form.is_valid():
            #import pdb; pdb.set_trace()
            #check if rules are accepted if not show message
            if form.cleaned_data['sepa_agree'] == True and \
                form.cleaned_data['rules_agree'] == True and \
                form.cleaned_data['privacy_agree'] == True:
                #check if member with this name already exists if not proceed
                if Member.objects.filter(
                                            name=preview_data['name'], 
                                            sirname=preview_data['sirname'], 
                                            email=preview_data['email']
                                        ).exists() == False:
                                            
                    member = Member()
                    member.name = preview_data['name']
                    member.sirname = preview_data['sirname']
                    member.street = preview_data['street']
                    member.streetnumber = preview_data['streetnumber']
                    member.postcode = preview_data['postcode']
                    member.location = preview_data['location']
                    member.country = preview_data['country']
                    member.email = preview_data['email']
                    member.phonenumber = preview_data['phonenumber']
                    member.birthdate = datetime.datetime.strptime(preview_data['birthdate'], '%d/%m/%Y')
                    member.entrydate = datetime.datetime.strptime(preview_data['entrydate'], '%d/%m/%Y')
                    member.fee = preview_data['fee']
                    member.iban = preview_data['iban']
                    member.bic = preview_data['bic']
                    member.bankname = preview_data['bankname']
                    member.memberstatus = preview_data['memberstatus']
                    member.status = 'pending'
                    member.sepa_agree = form.cleaned_data['sepa_agree']
                    member.rules_agree = form.cleaned_data['rules_agree']
                    member.privacy_agree = form.cleaned_data['privacy_agree']
                    member.save()
                    return render(request, 'register_status.html', {'status':'success'})
                    
                else:
                    try:
                        send_mail(
                            'Eigenbaukombinat Online Registrierung',
                            'Deine Registrierung für das Eigenbaukombinat ist erfolgreich eingegangen. Bitte habe noch etwas Geduld bis diese bestätigt wurde.',
                            SENDER_MAIL,
                            [member.email],
                            fail_silently=False,
                            )
                        send_mail(
                            'Eigenbaukombinat Online Registrierung',
                            'Ein neues Mitglied hat sich registriert',
                            SENDER_MAIL,
                            [MAIL],
                            fail_silently=False,
                            )
                    except:
                        return render(request, 'resgister_status.html',{'status':'notsend'})
                        
                    return render(request, 'register_status.html', {'status':'registered'})
            else:
                return render(request, 'register_preview.html', {'form':form, 'preview_data':preview_data, 'status':'failed'})
    
    form = AgreementForm()
    return render(request, 'register_preview.html', {'form':form})

def status(request):
    '''last page to show successfull registration and download registration data'''
    
    return render(request, 'register_status.html', {'status':'success'})
