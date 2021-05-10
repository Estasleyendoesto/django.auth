from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django import forms

from captcha.fields import CaptchaField


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email or Username')

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError('Esta cuenta está inactiva')


class RegisterForm(UserCreationForm):
    captcha = CaptchaField()
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')