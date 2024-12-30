import os
from pathlib import Path
import dj_database_url
from datetime import timedelta

# 1. Import django-environ
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Initialize environment variables
env = environ.Env()

# 3. Read the .env file
env.read_env(os.path.join(BASE_DIR, '.env'))

# 4. Now read the variables
SECRET_KEY = env('SECRET_KEY', default='fallback-secret-key')
DEBUG = env.bool('DEBUG', default=False)

# If you have multiple hosts, you can split them by comma
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'corsheaders',
    # Custom apps
    'utils',
    'master',
    'authuser',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'growupmore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'growupmore.wsgi.application'

# Database
DATABASE_URL = env('DATABASE_URL')
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

# Custom User Model
AUTH_USER_MODEL = 'authuser.User'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'authuser.authentication.CookieJWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.KendoPagination',
    'PAGE_SIZE': 10,
}

# Simple JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    # Cookies Configuration
    'TOKEN_COOKIE': 'access',  # Access token cookie name
    'TOKEN_COOKIE_SECURE': not DEBUG,
    'TOKEN_COOKIE_HTTP_ONLY': True,
    'TOKEN_COOKIE_SAMESITE': 'Lax',

    'REFRESH_TOKEN_COOKIE': 'refresh',  # Refresh token cookie name
    'REFRESH_TOKEN_COOKIE_SECURE': not DEBUG,
    'REFRESH_TOKEN_COOKIE_HTTP_ONLY': True,
    'REFRESH_TOKEN_COOKIE_SAMESITE': 'Lax',
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:9000",
]
CORS_ALLOW_CREDENTIALS = True

# Email Configuration using SendGrid
SENDGRID_API_KEY = env('SENDGRID_API_KEY', default='')

DEFAULT_FROM_EMAIL = "Grow Up More <info@growupmore.com>"

# SMS API Key
SMS_API_KEY = env('SMS_API_KEY', default='')

# Google reCAPTCHA settings
GOOGLE_RECAPTCHA_SECRET_KEY = env('GOOGLE_RECAPTCHA_SECRET_KEY', default='')
GOOGLE_RECAPTCHA_SITE_KEY = env('GOOGLE_RECAPTCHA_SITE_KEY', default='')
DISABLE_RECAPTCHA = env.bool('DISABLE_RECAPTCHA', default=False)

# OTP Configuration
OTP_EXPIRY_MINUTES = 15
OTP_MAX_ATTEMPTS = 5

# Login Configuration
MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCK_DURATION_HOURS = 24

# Resend OTP Configuration
MAX_RESEND_OTP_ATTEMPTS = 5
RESEND_OTP_LOCK_DURATION_MINUTES = 60

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
