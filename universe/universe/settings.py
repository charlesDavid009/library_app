"""
Django settings for universe project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=5pd&&4_^g*prtx*-&vpld2=0*$n$(d8$qn4wa1i_*q0n)st02'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ACTIONS = ['like', 'unlike', 'reblog', 'follow', 'unfollow', 'add', 'invite', 'comment', 'join', 'exit', 'confirm', 'reject','report', 'remove', 'pass']

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'accounts.MyUser'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3RD PARTY APPS
    'corsheaders',
    'rest_framework_swagger',
    'rest_framework',
    'rest_framework.authtoken',
    'taggit',
    'markdown_deux',
    'rest_framework_simplejwt',

    # Installed APPs
    'accounts',
    'blog',
    'groups',
    'news',
    'pages',
    'DMs',
    'profiles',
    'search',

]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware", 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'universe.urls'

#CORS_ORIGIN_ALLOW_ALL = True  

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

WSGI_APPLICATION = 'universe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

#jwt
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

#SIMPLE_JWT = {
#    'USER_ID_FIELD': 'MyUser.id'
#}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    #"DEFAULT_PARSER_CLASSES": [
        #"rest_framework.parsers.JSONParser",
    #],
    "DEFAULT_AUTHENTICATION_CLASSES": [                               # new
        "rest_framework.authentication.SessionAuthentication",        # new
        #"rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework_simplejwt.authentication.JWTTokenUserAuthentication",  # new
    ],
}