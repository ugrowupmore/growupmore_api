# settings.py

import os
import environ  # <-- NEW import
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Load .env file with python-dotenv (optional if you rely solely on django-environ)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------
# 1) Initialize django-environ with defaults
env = environ.Env(
    # Default types and values if they don't exist in .env
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    CORS_ALLOWED_ORIGINS=(list, []),
    CORS_ALLOW_CREDENTIALS=(bool, False),
    SECRET_KEY=(str, "change-me-in-prod"),
    DISABLE_RECAPTCHA=(bool, False),
    # Add more as needed...
)

# 2) Optionally read from a specific .env path
env_file = BASE_DIR / ".env"
if env_file.exists():
    env.read_env(str(env_file))
# ----------------------------------------------------

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")  # from .env or default

DEBUG = env.bool("DEBUG")       # "True"/"False" → Python bool

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")  # comma-separated string → list

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    # Local apps
    'utils',
    'authapp',
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
        'DIRS': [],  # add template directories if needed
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

# ----------------------------------------------------
# Database configuration using DATABASE_URL from .env
DATABASES = {
    'default': env.db("DATABASE_URL"),
}
# ----------------------------------------------------

AUTH_USER_MODEL = 'authapp.User'
AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# for deployment
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ----------------------------------------------------
# CORS
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_CREDENTIALS = env.bool("CORS_ALLOW_CREDENTIALS")
# ----------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authapp.authentication.JWTAuthenticationCookie',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
        'authapp.throttling.LoginRateThrottle',
        'authapp.throttling.OTPRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',
        'anon': '100/day',
        'login': '5/minute',  # Custom throttle scope for login
        'otp': '10/minute',   # Custom throttle scope for OTP-related requests
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',

    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# Secure Cookies Configuration
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# SameSite attribute for cookies
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# ===== SendGrid Configuration =====
SENDGRID_API_KEY = env("SENDGRID_API_KEY", default="")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="Grow Up More <info@growupmore.com>")

# ===== SMS API Configuration =====
SMS_API_KEY = env("SMS_API_KEY", default="")

# ===== Google reCAPTCHA Configuration =====
GOOGLE_RECAPTCHA_SECRET_KEY = env("GOOGLE_RECAPTCHA_SECRET_KEY", default="")
GOOGLE_RECAPTCHA_SITE_KEY   = env("GOOGLE_RECAPTCHA_SITE_KEY", default="")
DISABLE_RECAPTCHA           = env.bool("DISABLE_RECAPTCHA", default=False)

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'authuser': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'