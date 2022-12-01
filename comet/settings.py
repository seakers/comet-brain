"""
Django settings for comet project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-62-k*e0#rd(6l55%b)k+44ho7n^d7133+79toa%=62rg)ud8$#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*'
]

USE_X_FORWARDED_HOST = True



# Application definition

INSTALLED_APPS = [

    # Installed Packages
    'channels',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',

    # Comet APIs
    'comet',
    'comet_auth',
    'comet_assistant',
    'comet_problem'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'comet.HealthCheckMiddleware.HealthCheckMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'comet.urls'

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

WSGI_APPLICATION = 'comet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'comet',
        'USER': os.environ['SQL_USER'],
        'PASSWORD': os.environ['SQL_PASSWORD'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.environ['POSTGRES_PORT'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# CORS & CSRF

if os.environ['DEPLOYMENT_TYPE'] == 'aws':
    # CSRF_COOKIE_SECURE = True
    # CSRF_COOKIE_SAMESITE = 'None'
    CSRF_COOKIE_DOMAIN = '.selva-research.com'
    # SESSION_COOKIE_SECURE = True
    # SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_DOMAIN = '.selva-research.com'



CORS_ORIGIN_WHITELIST = (
    'http://daphne.engr.tamu.edu',
    'http://localhost:8080',
    'http://dev.selva-research.com',
    'http://prod.selva-research.com',
    'http://comet-bucket.selva-research.com',
    'http://comet-load-balancer-761241085.us-east-2.elb.amazonaws.com',
    'https://comet-load-balancer-761241085.us-east-2.elb.amazonaws.com',
    'http://comet-services.selva-research.com:8000',
    'https://comet-services.selva-research.com:443'
)

CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = (
    'http://daphne.engr.tamu.edu',
    'http://localhost:8080',
    'http://dev.selva-research.com',
    'http://prod.selva-research.com',
    'http://comet-bucket.selva-research.com',
    'http://comet-load-balancer-761241085.us-east-2.elb.amazonaws.com',
    'https://comet-load-balancer-761241085.us-east-2.elb.amazonaws.com',
    'http://comet-services.selva-research.com:8000',
    'https://comet-services.selva-research.com:443'
)


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.environ['REDIS_HOST'], os.environ['REDIS_PORT'])],
        }
    },
}

ASGI_APPLICATION = 'comet.asgi.application'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# AWS
DEPLOYMENT_TYPE = os.environ['DEPLOYMENT_TYPE']


##################
### Comet Path ###
##################
COMET_PATH = '/app'


#################
### NN Models ###
#################
NN_MODELS = {}
NN_MODELS_PATH = '/app/comet_assistant/assistant/models_copy'
LOAD_NN_MODELS = True
if LOAD_NN_MODELS is True:
    print('--> LOADING NN MODELS')
    import os
    from pathlib import Path
    from transformers import AutoModelForSequenceClassification
    model_dict = {}
    model_folder_path = Path(NN_MODELS_PATH)
    for file in os.scandir(model_folder_path):
        if file.is_dir():
            role_name = file.name
            role_model_path = model_folder_path / role_name
            loaded_model = AutoModelForSequenceClassification.from_pretrained(role_model_path)
            model_dict[role_name] = loaded_model
    NN_MODELS = model_dict
    print('--> FINISHED LOADING NN MODELS')


###########
### NLP ###
###########
import spacy
NLP_MODEL = spacy.load('en_core_web_sm')




LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s] - %(name)s - %(levelname)s - %(message)s'
        },
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y/%m/%d %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'debugging': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'config': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

