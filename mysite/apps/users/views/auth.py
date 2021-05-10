from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from ..forms import LoginForm
from ..models import User


class Login(LoginView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.request.user)

        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])


class Logout(LogoutView):
    next_page = 'home'


class Profile(TemplateView):
    template_name = 'auth/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(User, username=kwargs['username'])

        return context


class Account(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'auth/account.html'
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user