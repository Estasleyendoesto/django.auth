from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView 
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetView
from django.http.response import Http404
from django.urls import reverse_lazy


# Formulario de cambio de contraseña
# ---
class PasswordChange(PasswordChangeView):
    template_name = 'register/password_change.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        self.request.session['pass_has_changed'] = True
        return super().form_valid(form)


# Cambio de contraseña exitosa
# ---
class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'register/password_change_done.html'

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
    template_name = 'register/password_reset.html'
    email_template_name = 'register/password_reset_email.html'     # El email que recibe la persona
    subject_template_name = 'register/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def dispatch(self, *args, **kwargs):
        # Logged users cannot visit this view
        if self.request.user.is_authenticated:
            raise Http404('Es no va a ocurrir')

        return super().dispatch(*args, **kwargs)


# Template que notifica que el email ha sido enviado
# ---
class PasswordResetDone(PasswordResetCompleteView):
    template_name = 'register/password_reset_done.html'

    def dispatch(self, *args, **kwargs):
        # Logged users cannot visit this view
        if self.request.user.is_authenticated:
            raise Http404('Es no va a ocurrir')

        return super().dispatch(*args, **kwargs)


# Template para reestablecer la contraseña (formulario)
# ---
class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'register/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def dispatch(self, *args, **kwargs):
        # Logged users cannot visit this view
        if self.request.user.is_authenticated:
            raise Http404('Ya has reestablecido tu contraseña')

        return super().dispatch(*args, **kwargs)


# Template que notifica que se ha reestablecido la contraseña
# ---
class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'register/password_reset_complete.html'

    def dispatch(self, *args, **kwargs):
        # Logged users cannot visit this view
        if self.request.user.is_authenticated:
            raise Http404('Es no va a ocurrir')

        return super().dispatch(*args, **kwargs)