import pyotp
from django.db import models
from django.contrib.auth.models import User
from viewer.models import Location


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    locations = models.ManyToManyField(Location)
    verified = models.BooleanField(default=False)
    otp_key = models.CharField(max_length=150, default=pyotp.random_base32)





