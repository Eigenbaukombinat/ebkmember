from django.contrib import admin
from .models import *



class MemberAdmin(admin.ModelAdmin):
    list_display = ["surname", "name", "status"]

# Register your models here.
admin.site.register(Member, MemberAdmin)
