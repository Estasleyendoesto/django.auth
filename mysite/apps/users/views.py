from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetView
from django.http.response import Http404
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic import CreateView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect

from .forms import LoginForm, RegisterForm
from .models import User


class Login(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.request.user)

        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])


class Register(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.request.user)

        return super().dispatch(*args, **kwargs)


class Logout(LogoutView):
    next_page = 'home'


class Profile(TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(User, username=kwargs['username'])

        return context


class Account(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'users/account.html'
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordChange(PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        self.request.session['pass_has_changed'] = True
        return super().form_valid(form)


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'

    def get(self, request):
        # Nos aseguramos que el usuario no vuelva a esta vista
        try:
            if request.session['pass_has_changed']:
                del request.session['pass_has_changed']
        except KeyError:
            raise Http404('Es no va a ocurrir')

        return super().get(request)


# Solicitud para cambiar contraseña (introduce email y envía)
# ---
class PasswordReset(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'     # El email que recibe la persona
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            raise Http404('Es no va a ocurrir')

        return super().dispatch(*args, **kwargs)


# Template que notifica que el email ha sido enviado
# ---
class PasswordResetDone(PasswordResetCompleteView):
    template_name = 'users/password_reset_done.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            raise Http404('Es no va a ocurrir')

        return super().dispatch(*args, **kwargs)


# Template para reestablecer la contraseña
# ---
class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            raise Http404('Ya has reestablecido tu contraseña')

        return super().dispatch(*args, **kwargs)


# Template que indica que se ha reestablecido la contraseña
# ---
class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            raise Http404('Es no va a ocurrir')

        return super().dispatch(*args, **kwargs)
