from django.shortcuts import render

from rest_framework import generics, status, mixins, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone

from .models import User, OTP, FarmerProfile, OperatorProfile, OTP

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.exceptions import PermissionDenied, NotFound, AuthenticationFailed

from .serializers import (
    UserRegistrationSerializer,
    FarmerProfileSerializer,
    OperatorProfileSerializer,
    EmailOTPVerifySerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    FarmerUpdateSerializer,
    OperatorUpdateSerializer,
)

from rest_framework.views import APIView


# ==========================================================

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

# ===========================================================

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save() # This calls the create method in UserRegistrationSerializer

        refresh = TokenObtainPairSerializer.get_token(user)
        access = refresh.access_token

        return Response(
            {
                "message": "User registered successfully. Please proceed to fill your profile",
                "email": user.email,
                "role": user.role,
                "access": str(access),
                "refresh": str(refresh)
            },
            status=status.HTTP_201_CREATED
        )
class FarmerProfileCreateUpdateView(mixins.CreateModelMixin, generics.RetrieveUpdateAPIView):
    queryset = FarmerProfile.objects.all()
    serializer_class = FarmerProfileSerializer
    permission_classes = [IsAuthenticated] # User must be logged in

    def get_object(self):
        # Tries to retrieve the profile for the authenticated user.
        # If it doesn't exist, it doesn't raise a 404 immediately.
        # Instead, it indicates that an object was not found, which we'll handle in 'put'/'patch'.

        try:
            return self.request.user.farmerprofile
        except FarmerProfile.DoesNotExist:
            raise NotFound("Farmer profile not found for this user. Create it first using a POST request.")


    def post(self, request, *args, **kwargs):
        # Ensure the profile is created for the authenticated user and only if role is FARMER
        # This method handles the POST request to create a profile.
        # It's explicitly defined here because RetrieveUpdateAPIView typically expects GET/PUT/PATCH and we want to allow POST for creation.
        if self.request.user.role != User.Role.FARMER:
            raise PermissionDenied("Only users with 'FARMER' role can create a farmer profile.")
        # Check if a profile already exists for this user
        if hasattr(self.request.user, 'farmerprofile') and self.request.user.farmerprofile:
            return Response(
                {"detail": "A farmer profile already exists for this user. Use PUT/PATCH to update."},
                status=status.HTTP_409_CONFLICT
            )

        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
# ---------------------------------------------

    def put(self, request, *args, **kwargs):
        # Handle PUT (full update) for an existing profile
        if self.request.user.role != User.Role.FARMER:
            raise PermissionDenied("Only users with 'FARMER' role can update a farmer profile.")

        # Attempt to get the existing object for the user
        instance = self.get_object() # This will raise NotFound if not exists

        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

# ---------------------------------------------
    def patch(self, request, *args, **kwargs):
        # Handle PATCH (partial update) for an existing profile
        if self.request.user.role != User.Role.FARMER:
            raise PermissionDenied("Only users with 'FARMER' role can update a farmer profile.")

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # We also need to allow GET requests to retrieve the profile if it exists.
    # RetrieveUpdateAPIView already provides this via the 'get' method.

# ===========================================================
class OperatorProfileCreateUpdateView(mixins.CreateModelMixin, generics.RetrieveUpdateAPIView):
    queryset = OperatorProfile.objects.all()
    serializer_class = OperatorProfileSerializer
    permission_classes = [IsAuthenticated] # User must be logged in

    def get_object(self):
        try:
            return self.request.user.operatorprofile # Assumes reverse relation from User to OperatorProfile
        except OperatorProfile.DoesNotExist:
            raise NotFound("Operator profile not found for this user. Create it first using a POST request.")

    def post(self, request, *args, **kwargs):
        if self.request.user.role != User.Role.OPERATOR:
            raise PermissionDenied("Only users with 'OPERATOR' role can create an operator profile.")
        
        if hasattr(self.request.user, 'operatorprofile') and self.request.user.operatorprofile:
            return Response(
                {"detail": "An operator profile already exists for this user. Use PUT/PATCH to update."},
                status=status.HTTP_409_CONFLICT
            )
        
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def put(self, request, *args, **kwargs):
        if self.request.user.role != User.Role.OPERATOR:
            raise PermissionDenied("Only users with 'OPERATOR' role can update an operator profile.")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        if self.request.user.role != User.Role.OPERATOR:
            raise PermissionDenied("Only users with 'OPERATOR' role can update an operator profile.")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
class EmailOTPVerifyView(APIView):
    def post(self, request):
        serializer = EmailOTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": "Email verified successfully."}, status=status.HTTP_200_OK)

    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        
        

# Request password reset (send OTP to email)
# This handle sending an OTP to the user to reset their password.
class RequestPasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer       #Specifies the serializer that will validate incoming data

    def post(self, request):                            # Defines the POST method to handle the request when the user wants to reset their password.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)       #Checks if the data is valid.
        email = serializer.validated_data['email']      #Extracts the validated email field from the serializer for further processing
        try:
            user = User.objects.get(email=email)    # This Tries to find a user in the database with the matching email.
        except User.DoesNotExist:                   # If no such user exists, return a 404 response
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Generate OTP
        code = OTP.generate_otp()
        OTP.objects.create(user=user, code=code)        # Saves the generated OTP to the OTP table, linked to the user

        # This Simulate sending OTP (real app: send email/SMS)
        print(f"[DEBUG] OTP for {email} is {code}")

        return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)

# Confirm password reset using OTP
class ConfirmPasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        try:
            otp = OTP.objects.filter(user=user, code=code, is_used=False).latest('created_at')
        except OTP.DoesNotExist:
            return Response({"error": "Invalid or expired OTP."}, status=400)

        if otp.is_expired():
            return Response({"error": "OTP has expired."}, status=400)

        # Update password
        user.set_password(new_password)
        user.save()

        # Mark OTP as used
        otp.is_used = True
        otp.save()

        return Response({"message": "Password has been reset successfully."}, status=200)
    
# --- Farmer Profile Update ---
# This is a view for authenticated farmers to update their profile info.
class FarmerUpdateView(generics.UpdateAPIView):
    serializer_class = FarmerUpdateSerializer       # Uses a serializer that expects only the fields in the FarmerProfile model that can be updated.
    permission_classes = [permissions.IsAuthenticated]      
    def get_object(self):
        return self.request.user.farmerprofile


# --- Operator Profile Update ---
class OperatorUpdateView(generics.UpdateAPIView):
    serializer_class = OperatorUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.operatorprofile