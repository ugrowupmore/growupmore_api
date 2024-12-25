# settings.py

from pathlib import Path
import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    CORS_ALLOWED_ORIGINS=(list, []),
    CORS_ALLOW_ALL_ORIGINS=(bool, False),    
    GOOGLE_RECAPTCHA_SECRET_KEY=(str, ''),
    GOOGLE_RECAPTCHA_SITE_KEY=(str, ''),
    SENDGRID_API_KEY=(str, ''),          # Added
    DEFAULT_FROM_EMAIL=(str, ''),  
    # Add other environment variables with their default types here
)

# Reading .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Access the API key
GLOBAL_API_KEY = env("GLOBAL_API_KEY")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

# Allowed hosts
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

# Google reCAPTCHA configuration
GOOGLE_RECAPTCHA_SECRET_KEY = env("GOOGLE_RECAPTCHA_SECRET_KEY")
GOOGLE_RECAPTCHA_SITE_KEY = env("GOOGLE_RECAPTCHA_SITE_KEY")

# New setting
DISABLE_RECAPTCHA = env.bool("DISABLE_RECAPTCHA", default=False)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters', 
    'corsheaders', 
    'utils',
    'authuser',
    # 'master',
    # 'hr',
    # 'learn',
    # 'product',
    
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
        'DIRS': [],  # Add template directories here if needed
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

# Database configuration using DATABASE_URL from .env
DATABASES = {
    'default': env.db('DATABASE_URL'),  # Supabase PostgreSQL URL from .env
}

# If you are using multiple schemas
DATABASES['default']['OPTIONS'] = {
    'options': '-c search_path=public,authuser,master,hr,learn,product',
}

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.KendoPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'authuser.authentication.UnifiedJWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', 
    ),
}

# Simple JWT Configuration
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}


# CORS configuration
# CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=True)
# CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])

CORS_ALLOW_ALL_ORIGINS = True

# Password validation
AUTH_PASSWORD_VALIDATORS = []

# Internationalization settings
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

# SendGrid Email configuration (Removed Hostgator and Gmail settings)
SENDGRID_API_KEY = env("SENDGRID_API_KEY")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")

# Debugging (Remove in Production)
print(f"SENDGRID_API_KEY: {SENDGRID_API_KEY}")
print(f"DEFAULT_FROM_EMAIL: {DEFAULT_FROM_EMAIL}")

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


FRONTEND_BASE_URL = "http://127.0.0.1:9000"