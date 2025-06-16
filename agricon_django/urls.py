from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('/api/v1/register/')),
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('users.urls')),
]