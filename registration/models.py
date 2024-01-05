from django.db import models
from .choices import *
from django.utils import timezone
import datetime
from django_countries.fields import CountryField
from localflavor.generic.models import IBANField, BICField
from localflavor.generic.countries.sepa import IBAN_SEPA_COUNTRIES

class Member(models.Model):
    
    name = models.CharField(max_length = 150)
    surname = models.CharField(max_length = 250)
    street = models.CharField(max_length = 250)
    streetnumber = models.CharField(max_length = 10)
    postcode = models.CharField(max_length = 15)
    location = models.CharField(max_length = 250)
    country = CountryField(blank_label='Select Country')
    email = models.EmailField()
    phonenumber = models.CharField(max_length = 25)
    birthdate = models.CharField(max_length=30)
    entrydate = models.DateField(null=True)
    fee = models.FloatField()
    iban = IBANField(include_countries=IBAN_SEPA_COUNTRIES)
    memberstatus = models.CharField(max_length = 25, choices=MEMBERSTATUS)
    status = models.CharField(max_length = 25, choices=STATUS)
    sepa_agree = models.BooleanField(default=False, blank=False)
    rules_agree = models.BooleanField(default=False, blank=False)
    privacy_agree = models.BooleanField(default=False, blank=False)
    submitted = models.DateTimeField(blank=True, default=datetime.datetime.now)
    membernumber = models.CharField(max_length = 250, default='', null=True, blank=True)
    
    
