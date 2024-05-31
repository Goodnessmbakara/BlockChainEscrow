from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from rest_framework_simplejwt.tokens import RefreshToken

from src.models import Business
from .managers import CustomUserManager

AUTH_PROVIDERS = {'facebook':'facebook', 'google':'google',
                  'twitter':'twitter', 'email':'email'
                  }

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('exporter', 'Exporter'),
        ('importer', 'Importer'),
    ]
    username = models.CharField(max_length = 200, null =True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_type = models.CharField(max_length=255, choices=USER_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    auth_provider = models.CharField(max_length=255, blank=True,null = False, default=AUTH_PROVIDERS.get('email'))
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null =True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh =   RefreshToken.for_user(self)
        return {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token)
        }