from django.conf.urls import url

from . import views
from . import forms

member_forms = [
    		forms.MemberTypeForm,
    		forms.NormalMemberForm,
    		forms.CompanyMemberForm,
    	]

urlpatterns = [
    url( r'^$', views.MemberWizard.as_view(
    	member_forms,
    	condition_dict={'2': views.company_form_condition,
    		'1': views.normal_form_condition})),
]


