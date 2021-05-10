from django.views.generic.base import TemplateView

class AccountVerifyView(TemplateView):
    template_name = 'users/register_verify_done.html'
    email_template_name = 'users/register_verify_email.html'
    subject_template_name = 'users/register_verify_subject.txt'

    

