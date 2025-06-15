import random

import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

from datetime import timedelta
# ===========================================

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # Handles password hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# ========================================================

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True) # db_index for faster lookups
    is_verified = models.BooleanField(default=False)

    class Role(models.TextChoices):
        FARMER = 'FARMER', 'Farmer'
        OPERATOR = 'OPERATOR', 'Operator'
        ADMIN = 'ADMIN', 'Administrator'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.FARMER, # Default role for new registrations
        db_index=True # Indexing this for faster filtering by role
    )

    # Standard Django user fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    emailVerificationToken = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
    emailTokenExpires = models.DateTimeField(null=True, blank=True)
    emailVerified = models.BooleanField(default=False)
    
    passwordResetToken = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
    passwordTokenExpires = models.DateTimeField(null=True, blank=True)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


    objects = UserManager()

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['role']

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="users_set", # Changed from default 'user_set'
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="users_set",
        related_query_name="user",
    )


    def __str__(self):
        return self.email

# =============================================

class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmerprofile')
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True, db_index=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Farmer Profile for {self.user.email}"

# =============================================

class OperatorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='operatorprofile')
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True, db_index=True) 
    businessName = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Operator Profile for {self.user.email}"
# ===========================================
    
class OTP(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='otps')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))
