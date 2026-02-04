from django.contrib.auth.backends import ModelBackend
from myapp.models import MyUser


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, Token=None ** kwargs):
        try:
            user = MyUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except MyUser.DoesNotExist:
            return None
