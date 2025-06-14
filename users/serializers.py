from rest_framework import serializers
from .models import CustomUser, OTP

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'username', 'first_name', 'last_name', 'user_type', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data, is_verified=False)
        
        # Generate and save OTP
        otp_code = OTP.generate_otp()
        OTP.objects.create(user=user, code=otp_code)
        
        # Simulate sending OTP (real apps would send via SMS/email)
        print(f"OTP for {user.email} is {otp_code}")

        return user
