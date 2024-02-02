from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str("DJANGO_SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "django_filters",
    "drf_yasg",
    "rest_framework.authtoken",
    "src.apps.comments",
    "src.apps.lms",
    "src.apps.tasks",
    "src.apps.users",
    "src.apps.api_v1",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": env.str("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": env.str("POSTGRES_DB", "django"),
        "USER": env.str("POSTGRES_USER", "django"),
        "PASSWORD": env.str("POSTGRES_PASSWORD", ""),
        "HOST": env.str("DB_HOST", ""),
        "PORT": env.int("DB_PORT", 5432),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
}

DJOSER = {
    "LOGIN_FIELD": "email",
}

AUTH_USER_MODEL = "users.CustomUser"

# Swagger settings

BASE_REQUEST_URL = env.str("BASE_REQUEST_URL")

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {"type": "basic"},
        "Token": {"type": "apiKey", "name": "Authorization", "in": "header"},
    },
    "DEFAULT_AUTO_SCHEMA_CLASS": "src.apps.swagger.auto_schema_tags.CustomAutoSchema",
}

EMPLOYEE_NAME_LENGTH = 64
USERNAME_LENGTH = 64
EMAIL_LENGTH = 64
ROLE_NAME_LENGTH = 64
GRADE_NAME_LENGTH = 64
POSITION_NAME_LENGTH = 64

NAME_FIELD_LENGTH = 256
MIN_SKILLS_ASSESSMENT = 0
MAX_SKILLS_ASSESSMENT = 5
DEFAULT_ASSESSMENT_BEFORE = 0
DEFAULT_ASSESSMENT_AFTER = 3
STATUS_FIELD_LENGTH = 16
TEXT_FIELD_LENGTH = 2048

# corsheaders
CORS_ALLOW_ALL_ORIGINS = True

try:
    from .local_settings import *
except ImportError:
    pass
