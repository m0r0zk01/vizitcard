from django.contrib.auth.backends import BaseBackend
from app.models import User


class EmailAuthentication(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        user = User.objects.get(email=username)
        password_valid = user.check_password(password)
        if user and password_valid:
            return user
        return None

    def get_user(self, user_id):
        return User.objects.get(pk=user_id)
