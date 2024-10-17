import os
from datetime import timedelta
from enum import Enum
from pathlib import Path
from typing import Any

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class EnvironmentOption(Enum):
    DEVELOPMENT = 1
    TESTING = 2
    STAGING = 3
    PRODUCTION = 4

    @classmethod
    def get(cls, env: str) -> "EnvironmentOption":
        for option in cls:
            if option.name.lower() == env.lower():
                return option
        raise ValueError(f"Invalid environment option: {env}")

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, EnvironmentOption):
            return self.value < other.value
        return False

    def __le__(self, other: Any) -> bool:
        if isinstance(other, EnvironmentOption):
            return self.value <= other.value
        return False

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, EnvironmentOption):
            return self.value > other.value
        return False

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, EnvironmentOption):
            return self.value >= other.value
        return False

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, EnvironmentOption):
            return self.value == other.value
        return False


ENVIRONMENT = EnvironmentOption.get(os.environ.get("ENVIRONMENT", "TESTING"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-ptj_a$2tl7at!_uh=m*j@3uk73tf)p!#hvc@ejztula$8jdt(3")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 1


DATABASE_URL = "sqlite:///test.db3"

if ENVIRONMENT == EnvironmentOption.DEVELOPMENT:
    DATABASE_URL = os.environ.get("DEVELOPMENT_DATABASE_URL", DATABASE_URL)

if ENVIRONMENT == EnvironmentOption.PRODUCTION:
    DATABASE_URL = os.environ.get("PRODUCTION_DATABASE_URL", DATABASE_URL)


ALLOWED_HOSTS: list[Any] = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",
    "rest_framework",
    "rest_framework_simplejwt",
    "scheduler",
]
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "tokenUrl": "http://127.0.0.1:8000/api_v1/auth/token/",
            "flow": "accessCode",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'",
        },
    },
    "USE_SESSION_AUTH": False,
    "SECURITY_REQUIREMENTS": [{"Bearer": []}],
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "scheduler_app.urls"

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

WSGI_APPLICATION = "scheduler_app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {"default": dj_database_url.config(default=DATABASE_URL)}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
