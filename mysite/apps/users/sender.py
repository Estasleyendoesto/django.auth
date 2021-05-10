from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.auth import login
from django.template import loader

from .models import User
from .token import account_activation_token


def account_verify(user, request):
    user.is_active = False
    user.save()

    # Extract and Gerenate important info
    current_site = get_current_site(request)
    uid          = urlsafe_base64_encode( force_bytes(user.pk) )
    token        = account_activation_token.make_token(user)
    protocol     = 'https' if request.is_secure() else 'http'

    send_email(user, current_site, uid, token, protocol)


def send_email(user, current_site, uid, token, protocol):
    subject = 'Validación de registro para %s' % current_site.name
    message = loader.render_to_string('signup/signup_email_verify.html', {
        'user'    : user,
        'uid'     : uid,
        'token'   : token,
        'protocol': protocol,
        'domain'  : current_site.domain
    })
    email   = EmailMessage(subject, message, to=[user.email] )

    email.send()


def check_token(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)