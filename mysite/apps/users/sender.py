
def account_verify(user, request):
    user.is_active = False
    user.save()

    


def send_email():
    pass