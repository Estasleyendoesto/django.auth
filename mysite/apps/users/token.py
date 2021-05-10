from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int

from django.conf import settings

class AccountVerifyTokenGenerator(PasswordResetTokenGenerator):
    
    def check_token(self, user, token):
        """
        Check that a account validation token is correct for a given user.
        """
        if not (user and token):
            return False

        # Parse the token
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            return False

        # EMAIL_VERIFY_TIMEOUT inject
        if (self._num_seconds(self._now()) - ts) > settings.EMAIL_VERIFY_TIMEOUT:
            return False

        return True

account_activation_token = AccountVerifyTokenGenerator()