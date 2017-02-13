from django.db import models
from .choices import *
from django.utils import timezone
import datetime

class Member(models.Model):
    
    name = models.CharField(max_length = 150)
    sirname = models.CharField(max_length = 250)
    sex = models.CharField(max_length = 25, choices=SEX)
    street = models.CharField(max_length = 250)
    streetnumber = models.CharField(max_length = 10)
    postcode = models.CharField(max_length = 15)
    location = models.CharField(max_length = 250)
    country = models.CharField(max_length = 250)
    email = models.EmailField()
    phonenumber = models.CharField(max_length = 25)
    birthdate = models.DateField()
    entrydate = models.DateField()
    fee = models.FloatField()
    iban = models.CharField(max_length = 34)
    bic = models.CharField(max_length = 11)
    bankname = models.CharField(max_length = 250)
    memberstatus = models.CharField(max_length = 25, choices=MEMBERSTATUS)
    status = models.CharField(max_length = 25, choices=STATUS)
    sepa_agree = models.BooleanField(default=False, blank=False)
    rules_agree = models.BooleanField(default=False, blank=False)
    privacy_agree = models.BooleanField(default=False, blank=False)
    submitted = models.DateTimeField(blank=True, default=datetime.datetime.now)
    
    
