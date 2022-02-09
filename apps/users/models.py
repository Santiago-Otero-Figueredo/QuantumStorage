from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from apps.core.models import QuantumStorageModel

class User(AbstractBaseUser, PermissionsMixin, QuantumStorageModel):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True,  null=True, blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = BaseUserManager()

    def __str__(self):
        return f"{self.email}"

    @staticmethod
    def create_user(username, email, password=None, **kwargs):
        """Create and return a User with an email, phone number, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')

        user = User.objects.create(username=username, email=BaseUserManager.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    @staticmethod
    def get_by_email(email: str):
        """Get user instance by email"""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None