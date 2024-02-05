import os
from datetime import timedelta
from pathlib import Path
from django.contrib import messages
from benny_dealz.third_parties.cloudinary import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# CSRF_TRUSTED_ORIGINS = []
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", 1)))

ALLOWED_HOSTS = ["*"] if DEBUG else [".vercel.app"]
# CSRF_TRUSTED_ORIGIN = [f"https://{config('HOST_NAME')}"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Core Apps
    "apps.cars",
    "apps.dealers",
    "apps.accounts",
    "apps.profiles",
    "apps.wallet",
    "apps.notifications",
    "apps.transactions",
    # 3rd party
    'rest_framework',
    'widget_tweaks',
    "phone_field",
    'cloudinary',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'benny_dealz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'benny_dealz.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DB_USERNAME = config("POSTGRES_USER")
DB_PASSWORD = config("POSTGRES_PASSWORD")
DB_DATABASE = config("POSTGRES_DB")
DB_HOST = config("POSTGRES_HOST")
DB_PORT = config("POSTGRES_PORT")
DB_IS_AVAIL = all([
    DB_USERNAME,
])

POSTGRES_READY = str(config('POSTGRES_READY')) == "1"

if DB_IS_AVAIL and POSTGRES_READY:
    DATABASES = {
        "default": {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DB_DATABASE,
            'USER': DB_USERNAME,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT
        }
    }
print(DATABASES)

PROTOCOL = 'https'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'FETCH_USERINFO': True,
        'APP': {
            'client_id': config("GOOGLE_AUTH_CLIENT_ID"),
            'secret': config("GOOGLE_AUTH_SECRET"),
        },
        'SCOPE': [
            'profile',
            'email',
            'openid'
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline'
        }
    }
}

SITE_ID = 1

SOCIALACCOUNT_LOGIN_ON_GET = True

# Default authentication model...
AUTH_USER_MODEL = "accounts.User"

# Login url...
LOGIN_URL = 'accounts/login'

LOGIN_REDIRECT_URL = 'home'

LOGOUT_REDIRECT_URL = 'home'

ACCOUNT_LOGOUT_ON_GET = True

SOCIALACCOUNT_LOGIN_ON_GET = True

# Login redirect url...
PASSWORD_RESET_DOMAIN = f'{PROTOCOL}://{ALLOWED_HOSTS[0]}'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
MEDIA_DIRS = [BASE_DIR / "media"]

# Email Settings...
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = config('EMAIL_USE_SSL')
SUPPORT_EMAIL = config('SUPPORT_EMAIL')

# Django RESTFUL API authentication settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 6
}

# Django RESTFUL API JWT settings
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": (
        "Bearer",
        "JWT",
    ),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'SIGNING_KEY': "os.environ.get('SIGNING_KEY')",
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ORIGIN_ALLOW_ALL = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GOOGLE_MAPS_API_KEY = "YOU_SECRET_KEY"

# This validates the file size...
FILE_UPLOAD_PERMISSION = 0o640

MESSAGE_TAGS = {
    messages.ERROR: "danger"
}
