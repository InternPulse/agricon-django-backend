from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    UserRegistrationView,
    CustomTokenObtainPairSerializer,
    TokenObtainPairView,
    TokenRefreshView,
    FarmerProfileCreateUpdateView,
    OperatorProfileCreateUpdateView,
    EmailOTPVerifyView,
    LogoutView,
    RequestPasswordResetView,
    ConfirmPasswordResetView,
    FarmerUpdateView,
    OperatorUpdateView,
)

urlpatterns = [
    # User Registration Endpoint
    path('auth/register/', UserRegistrationView.as_view(), name='register'),

    # This endpoint takes email and password, returns access and refresh tokens
    path('auth/login/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    path('verify-email-otp/', EmailOTPVerifyView.as_view(), name='verify-email-otp'),

    # This endpoint takes a refresh token, returns a new access token (and new refresh if rotation is on==currently on)
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profile Endpoints
    path('auth/profile/farmer/', FarmerProfileCreateUpdateView.as_view(), name='farmer_profile'),
    path('auth/profile/operator/', OperatorProfileCreateUpdateView.as_view(), name='operator_profile'),

    # Logout Endrpoint
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Password-reset Endpoint
    path('password-reset/request/', RequestPasswordResetView.as_view()),
    
    # Endpoint for confirm password-reset
    path('password-reset/confirm/', ConfirmPasswordResetView.as_view()),
    
    # Farmer update Endpoint
    path('farmer/update/', FarmerUpdateView.as_view()),
    
    # Operator update Endpoint
    path('operator/update/', OperatorUpdateView.as_view()),
    
    
]