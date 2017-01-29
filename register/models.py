from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from localflavor.generic.countries.sepa import IBAN_SEPA_COUNTRIES
from localflavor.generic.models import IBANField, BICField
import datetime


FEETYPES = (
    ('normal;24', 'Normal – 24€ / Monat'),
    ('discount;18', 'Ermäßigt – 18€ / Monat'),
    ('junior;8', 'Junior – 8€ / Monat'),
    ('company;100', 'Firma/Institution – 100€ / Monat'),
    ('custom', 'anderer'),
)


MEMBERTYPES = (
    ('normal', 'ordentliche Mitgliedschaft'),
    ('foerder', 'Fördermitgliedschaft'),
    ('firma', 'Firmenmitgliedschaft'),
)


class MemberRegistration(models.Model):
    '''model for member registrations'''
   
    membertype = models.CharField(
        max_length=10, choices=MEMBERTYPES, default='normal')
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=150)
    company = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200)
    postcode = models.CharField(max_length=10)
    country = CountryField(default='DE', blank=True)
    email = models.EmailField()
    birthdate = models.DateTimeField(blank=True, null=True)
    entrydate = models.DateTimeField(blank=True, default=datetime.date.today)
    submitted_dt = models.DateTimeField(blank=True, default=datetime.datetime.now)
    fee = models.CharField(choices=FEETYPES, default='normal', max_length=100)
    customfee = models.PositiveIntegerField(blank=True, null=True)
    iban = IBANField(include_countries=IBAN_SEPA_COUNTRIES)
    #bic = BICField()
    sepa_agree = models.BooleanField()
    
