from rest_framework import serializers
from django.db import transaction # for atomic operations
from django.utils import timezone
from .models import User, FarmerProfile, OperatorProfile, OTP
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth import password_validation, authenticate
from django.utils.translation import gettext_lazy as _

from utils.email import send_welcome_email


class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = ['id', 'firstName', 'lastName', 'phone', 'address']
        read_only_fields = ['user']

class OperatorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatorProfile
        fields = ['id', 'firstName', 'lastName', 'phone', 'businessName', 'address']
        read_only_fields = ['user']

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        max_length=255,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.'
        }
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'},
        error_messages={
            'required': 'Password is required.',
            'min_length': 'Password must be at least 8 characters long.'
        }
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'},
        error_messages={
            'required': 'Password confirmation is required.',
            'min_length': 'Password confirmation must be at least 8 characters long.'
        }
    )
    role = serializers.ChoiceField(
        choices=User.Role.choices,
        required=True,
        error_messages={
            'required': 'Role is required.',
            'invalid_choice': 'Invalid role provided.'
        }
    )


    class Meta:
        fields = ['email', 'password', 'password2', 'role']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "Passwords do not match."})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})

        return data

    @transaction.atomic
    def create(self, validated_data):
        
        validated_data.pop('password2') # Pop password2, not a model field

        # Create the User instance
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            is_verified=False
        )
        
        # Generate and save OTP
        otp_code = OTP.generate_otp()
        OTP.objects.create(user=user, code=otp_code)
        
        # Simulate sending OTP (real apps would send via SMS/email)
        print(f"OTP for {user.email} is {otp_code}")

        send_welcome_email(user.email)

        return user, otp_code
    

# =====================================
# Customized TokenObtainPairSerializer to add user role to token payload
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.emailVerified:
            raise AuthenticationFailed("Please verify your email before logging in.")

        # Include extra claims in the token response
        data['email'] = self.user.email
        data['role'] = self.user.role
        return data   

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['role'] = user.role

        return token

# =====================================    
class EmailOTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        try:
            otp = OTP.objects.filter(user=user, code=code, is_used=False).latest("created_at")
        except OTP.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired OTP.")

        if otp.is_expired():
            raise serializers.ValidationError("OTP has expired.")

        # Mark OTP as used
        otp.is_used = True
        otp.save()

        # Mark user as verified
        user.emailVerified = True
        user.is_verified = True  # in case you use both
        user.save()

        return attrs
    
    
# --- FORGOT PASSWORD VIA OTP ---

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({"new_password2": _("The two new passwords do not match.")})

        try:
            password_validation.validate_password(data['new_password1'], self.context['request'].user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"new_password1": list(e.messages)})

        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Your old password was entered incorrectly. Please enter it again."))
        return value