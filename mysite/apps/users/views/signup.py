from django.views.generic.base import TemplateView
from django.views.generic import CreateView

from django.http.response import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy

from ..sender import account_verify
from ..forms import RegisterForm


class Signup(CreateView):
    template_name = 'signup/signup.html'
    form_class    = RegisterForm
    success_url   = reverse_lazy('signup_complete')

    def dispatch(self, *args, **kwargs):
        # Loggin users cannot register!
        if self.request.user.is_authenticated:
            return redirect(self.request.user)

        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        self.request.session['account_has_register'] = True
        
        # Account verify Injection Script
        account_verify(self.object, self.request)
        return super().get_success_url()

    
class SignupComplete(TemplateView):
    template_name = 'signup/signup_complete.html'

    def get(self, request):
        # Nos aseguramos que el usuario no vuelva a esta vista
        try:
            if request.session['account_has_register']:
                del request.session['account_has_register']
        except KeyError:
            raise Http404('Es no va a ocurrir')

        return super().get(request)


"""
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.template import loader
"""


"""
class Register(CreateView):
    template_name = 'users/register_confirm.html'
    email_template_name = 'users/register_verify_email.html'
    subject_template_name = 'users/register_verify_subject.txt'
    form_class = RegisterForm
    success_url = reverse_lazy('register_complete')

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.request.user)

        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        self.object.is_active = False

        meta = {
            'user': self.object,
            'domain': get_current_site(self.request).domain,
            'sitename': get_current_site(self.request).name,
            'uid': urlsafe_base64_encode(force_bytes(self.object.pk)),
            'token': account_activation_token.make_token(self.object),
            'email_template': self.email_template_name,
            'subject_template': self.subject_template_name
        }

        self.verify_account( kwargs = meta )

        return super().get_success_url()

    def verify_account(self, **kwargs):
        subject = loader.render_to_string('users/register_verify_subject.txt', {'site_name': kwargs['sitename']})
        message = loader.render_to_string(kwargs['email_template'], {
            'user': kwargs['user'],
            'domain': kwargs['domain'],
            'uid': kwargs['uid'],
            'token': kwargs['token']
        })

        email = EmailMessage(subject, message, to=[ kwargs['user'].email ])
        email.send()





class RegisterVerify(TemplateView):
    template_name = 'users/register_verify_done.html'
    
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)

        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

"""