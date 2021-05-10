from threading import Thread

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from .errors import InvalidUserModel
from .token import default_token_generator

from django.contrib.sites.models import Site

from django.urls import reverse

def send_email(user, thread=True, **kwargs):
    try:
        user.save()

        expiry_ = kwargs.get('expiry')
        token, expiry = default_token_generator.make_token(user, expiry_)

        sender = 'noreply@aliasaddress.com'
        domain = Site.objects.get_current().domain
        subject = 'Email verify on %s' % Site.objects.get_current().name
        mail_plain = 'users/register_verify_email.txt'
        mail_html = 'users/register_verify_email.html'

        args = (user, token, expiry, sender, domain, subject, mail_plain, mail_html)
        if thread:
            t = Thread(target=send_email_thread, args=args)
            t.start()
        else:
            send_email_thread(*args)
    except AttributeError:
        raise InvalidUserModel('The user model you provided is invalid')


def send_email_thread(user, token, expiry, sender, domain, subject, mail_plain, mail_html):

    link = domain + reverse('register_verify', args=[token])

    context = {'link': link, 'expiry': expiry, 'user': user}

    text = render_to_string(mail_plain, context)

    html = render_to_string(mail_html, context)

    msg = EmailMultiAlternatives(subject, text, sender, [user.email])
    msg.attach_alternative(html, 'text/html')
    msg.send()


def verify_token(token):
    valid, user = default_token_generator.check_token(token)
    if valid:
        user.is_active = True
        user.last_login = timezone.now()
        user.save()
        return valid, user
    return False, None