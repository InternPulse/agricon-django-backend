from pathlib import Path
import os
import environ
from datetime import timedelta
import dj_database_url
from decouple import config
from corsheaders.defaults import default_headers

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False),
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'users',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://agricon-ng.vercel.app",
    "https://agricon.com.ng"
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    'Authorization',
]

ROOT_URLCONF = 'agricon_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'agricon_django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASE_URL = config('DATABASE_URL')

DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
}

# SENDGRID API CONFIGURATION

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 100 # Good for production
            }
        },
        "KEY_PREFIX": "agricon_cache"
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer', # Optional: enabled for browsable API in dev
    ),

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),

    'DEFAULT_THROTTLE_CLASSES': [
         'rest_framework.throttling.AnonRateThrottle',
         'rest_framework.throttling.UserRateThrottle',
         ],
    
     'DEFAULT_THROTTLE_RATES': {
        # Default rates for global DEFAULT_THROTTLE_CLASSES:
        'anon': '100/day',
        'user': '1000/day',

        # Specific rates for OTP and Login endpoints:
        'otp_anon_request': '3/minute',  # Max 3/min/ip
        'otp_user_request': '5/minute',  # Max 5 OTP requests/min (for resend)
        'login_anon_attempt': '5/minute', # Max 5 attempts/min/ip
        'otp_verify_anon': '5/minute',  # Max 5 OTP verification/min/ip
        'signup_anon_request': '5/hour',  # Max 5 signups/hour/ip
    },
}



SIMPLE_JWT = {
   
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=600),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),

    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": env('SECRET_KEY'),
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",

    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",

    # JTI Claim: For blacklisting specific tokens
    "JTI_CLAIM": "jti", 

    # Default Serializers/Views: Pointers to Simple JWT's built-in components
    # Customized TokenObtainPairSerializer later to add user role to payload
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.token_blacklist.serializers.BlacklistedTokenSerializer",
    "TOKEN_OBTAIN_PAIR_CLASS": "rest_framework_simplejwt.views.TokenObtainPairView",
    "TOKEN_REFRESH_CLASS": "rest_framework_simplejwt.views.TokenRefreshView",
    "TOKEN_VERIFY_CLASS": "rest_framework_simplejwt.views.TokenVerifyView",
    "TOKEN_BLACKLIST_CLASS": "rest_framework_simplejwt.views.TokenBlacklistAPIView",

    
    "UPDATE_LAST_LOGIN": False,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None, # not needed for HS256
    "LEEWAY": 0,

    # "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5), 
    # "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
}

AUTH_USER_MODEL = 'users.User'
