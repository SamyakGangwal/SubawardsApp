from django.contrib.auth.models import User

from subawardBackend.models import CustomUser
class UsernameAuthBackend:
    """
    Custom authentication backend.

    Allows users to log in using their username.
    """

    def authenticate(self, request, username=None, password=None):
        """
        Overrides the authenticate method to allow users to log in using their username.
        """
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                return user
            return None
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Overrides the get_user method to allow users to log in using their email address.
        """
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None