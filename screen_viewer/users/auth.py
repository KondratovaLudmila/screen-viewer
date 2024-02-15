from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.views.decorators.debug import sensitive_variables
from django.core.exceptions import PermissionDenied
from services.otp_handler import totp_handler

class OTPBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, verify=False, **kwargs):
        
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if verify and totp_handler.check_otp(user.profile.otp_key, password):
                totp_handler.clean_up(username)
                return user
            if not user.profile.verified and user.check_password(password):
                return user
            if user.profile.verified and totp_handler.check_otp(user.profile.otp_key, password):
                return user
        
        raise PermissionDenied

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
    
    