from .models import MemberRegistration
from formtools.wizard.views import SessionWizardView
from django.shortcuts import render


def company_form_condition(wizard):
    # try to get the cleaned data of step 1
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    # check if the field ``leave_message`` was checked.
    return cleaned_data.get('membertype') == 'firma'

def normal_form_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    # check if the field ``leave_message`` was checked.
    return cleaned_data.get('membertype') == 'normal'


class MemberWizard(SessionWizardView):

    def done(self, form_list, **kwargs):
        #XXX mails verschicken etc...
        return render(self.request, 'done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })