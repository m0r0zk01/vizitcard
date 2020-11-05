from django.contrib.auth.backends import BaseBackend
from PROJECT.app.models import User


class EmailAuthentication(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        return User.objects.get(pk=user_id)
