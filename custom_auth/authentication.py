from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except user_model.DoesNotExist:
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None

