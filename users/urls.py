from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    UserRegistrationView,
    CustomTokenObtainPairSerializer,
    TokenObtainPairView,
    TokenRefreshView,
    FarmerProfileCreateUpdateView,
    OperatorProfileCreateUpdateView
)

urlpatterns = [
    # User Registration Endpoint
    path('auth/register/', UserRegistrationView.as_view(), name='register'),

    # This endpoint takes email and password, returns access and refresh tokens
    path('auth/login/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),

    # This endpoint takes a refresh token, returns a new access token (and new refresh if rotation is on==currently on)
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profile Endpoints
    path('auth/profile/farmer/', FarmerProfileCreateUpdateView.as_view(), name='farmer_profile'),
    path('auth/profile/operator/', OperatorProfileCreateUpdateView.as_view(), name='operator_profile'),
]