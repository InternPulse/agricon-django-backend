from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    UserRegistrationView,
    LoginViewWithThrottling,
    TokenRefreshView,
    FarmerProfileCreateUpdateView,
    OperatorProfileCreateUpdateView,
    EmailOTPVerifyView,
    LogoutView,
    RequestPasswordResetView,
    ConfirmPasswordResetView,
    ResendOTPView,
    ChangePasswordView,
    PasswordResetRequestView,
    ContactUsView
)

urlpatterns = [
    # User Registration Endpoint
    path('register/', UserRegistrationView.as_view(), name='register'),

    # This endpoint takes email and password, returns access and refresh tokens
    path('login/', LoginViewWithThrottling.as_view(), name='token_obtain_pair'),
    path('verify-email-otp/', EmailOTPVerifyView.as_view(), name='verify-email-otp'),

    # This endpoint takes a refresh token, returns a new access token (and new refresh if rotation is on==currently on)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profile Endpoints
    path('profile/farmer/', FarmerProfileCreateUpdateView.as_view(), name='farmer_profile'),
    path('profile/operator/', OperatorProfileCreateUpdateView.as_view(), name='operator_profile'),

    # Change Password Endpoint
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),

    # Logout Endpoint
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Password-reset Endpoint
    path('password-reset/request/', RequestPasswordResetView.as_view()),
    
    #Endpoint for resending OTP 
    path('otp/resend/', ResendOTPView.as_view()),
    
    # Endpoint for confirm password-reset
    path('password-reset/confirm/', ConfirmPasswordResetView.as_view()),

    # Endpoint for forgot password and confirm new password
    path('forgot-password/', PasswordResetRequestView.as_view(), name='forgot_password'),

    # Endpoint for contact us
    path('contact-us/', ContactUsView.as_view(), name='contact_us'),
]