from django.views.generic.base import TemplateView
from django.views.generic import CreateView

from django.http.response import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy

from ..sender import account_verify, check_token
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


class SignupEmailConfirm(TemplateView):
    template_name = 'signup/signup_account_verified.html'

    def get(self, request, uidb64, token):
        # Si el token es válido, activamos cuenta y login
        check_token(request, uidb64, token)

        return super().get(request)