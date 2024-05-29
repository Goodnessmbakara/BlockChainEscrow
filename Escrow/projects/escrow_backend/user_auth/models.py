from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from src.models import Business
# Create your models here.

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser):
    USER_TYPE_CHOICES = [
        ('experter', 'Experter'),
        ('importer', 'Importer'),
    ]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null =True)
    user_type = models.CharField(max_length=255, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    