from rest_framework import serializers
from django.db import transaction # for atomic operations
from django.utils import timezone
from .models import User, FarmerProfile, OperatorProfile, OTP

class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = ['firstName', 'lastName', 'phone', 'address']
        read_only_fields = ['user']

class OperatorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatorProfile
        fields = ['firstName', 'lastName', 'phone', 'businessName', 'address']
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

    # Nested serializers for profiles
    # farmer_profile = FarmerProfileSerializer(required=False, allow_null=True)
    # operator_profile = OperatorProfileSerializer(required=False, allow_null=True)

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

        return user
    
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