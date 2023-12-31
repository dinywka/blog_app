"""
Django settings for django_settings project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
# import environ
import os



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# env = environ.Env(
#     EMAIL_HOST=(str, None),
#     EMAIL_HOST_USER=(str, None),
#     EMAIL_HOST_PASSWORD=(str, None),
# )
# environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-coc79ha1i1m_4qwoag1&x1yq1y6mk1kzsjyjm0t!t*_*l-jftl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ditim.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    "grappelli",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog_app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_settings.urls'

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

WSGI_APPLICATION = 'django_settings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "django_ram_cache_table",
    },
    "extra": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache_db_table",
        "TIMEOUT": "120",
        "OPTIONS": {
            # "MAX_ENTIES": 200,
        },
    },
}

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

LANGUAGE_CODE = 'ru'

TIME_ZONE = "Etc/GMT-6"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = "/static/"
# if DEBUG:
#     # режиме разработки: django "отдаёт" статику сам
#     STATICFILES_DIRS = [
#         Path(BASE_DIR / "static"),
#         Path(BASE_DIR / "static_external"),
#     ]
# else:
#     # режиме production(debug==false): nginx "отдаёт" статику
#     # collectstatic
#     STATIC_ROOT = Path(BASE_DIR / "static")
#     STATICFILES_DIRS = [
#         Path(BASE_DIR / "static_external"),
#     ]
#
# MEDIA_URL = "media/"
# MEDIA_ROOT = "static/media"

MEDIA_ROOT = '/home/ditim/blog_app/media'
MEDIA_URL = '/media/'
STATIC_ROOT = '/home/ditim/blog_app/static'
STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = 465  # (465 = SSL | 587 = TLS)
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
# EMAIL_HOST_USER = env("EMAIL_HOST_USER")  # Ваш адрес Yandex
# EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")  # Пароль от вашего Yandex аккаунта

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
