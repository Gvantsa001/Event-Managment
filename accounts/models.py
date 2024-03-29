from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from .managers import UserManager

AUTH_PROVIDERS = {'email': 'email'}

class User(AbstractUser,PermissionsMixin):
    id = models.BigAutoField(primary_key=True,editable=False)
    email = models.EmailField(max_length=255,verbose_name=_("Email address"),unique=True)
    first_name = models.CharField(max_length=255,verbose_name=_("First name"))
    last_name = models.CharField(max_length=255,verbose_name=_("Last name"))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length=55, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))
    is_event_manager = models.BooleanField(default=False, verbose_name=_("Event manager"))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = UserManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
         }


    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.user.first_name}"




