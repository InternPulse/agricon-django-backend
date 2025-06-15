from django.shortcuts import render

from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User, FarmerProfile, OperatorProfile, OTP

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework.exceptions import PermissionDenied, NotFound

from .serializers import (
    UserRegistrationSerializer,
    FarmerProfileSerializer,
    OperatorProfileSerializer
)

# ==========================================================

# Customized TokenObtainPairSerializer to add user role to token payload
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
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