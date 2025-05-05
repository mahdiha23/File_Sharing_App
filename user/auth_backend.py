from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class PhoneAuthBackend(ModelBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(phone=phone)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
