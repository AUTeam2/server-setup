"""
Django settings for webinterface project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cfh16z33oa@=vl^*5mfhsy&#4b6()l^usx3l#xo8llo)d=g6ox'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.99.100',
    'auteam2.mooo.com',
    '119.74.164.55',
    '192.168.1.7',
    'webinterface',
    '192.168.0.16',
    'elab.ase.au.dk'
]

# Application definition

INSTALLED_APPS = [
    'comms',
    'demo_module',
    'django_crontab',
    'database_poc',
    'homepage',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
]

# Crispy templates support form validation and rendering using Bootstrap V4
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Cronjob is set with the command "python manage.py crontab add" and will start with the server.
# An already set Cronjob is removed with the command "python manage.py crontab remove".
# For the changes to be taken into account, the server needs to be restarted after a command have been given.
CRONJOBS = [
    # The scheduler is set to run the command "Database_clean_up" every minute of all hours of the day
    ('*/1 * * * *', 'database_poc.cron.Database_clean_up', '2>&1'),
    ('*/1 * * * *', 'demo_module.cron.Database_clean_up', '2>&1'),
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

ROOT_URLCONF = 'webinterface.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'webinterface.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# These values must match the docker-compose file
# Change these to environment variables once the setup is stable
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'webinterface_dev',
        'USER': 'team2',
        'PASSWORD': 'team2',
        'HOST': 'db',
        'PORT': '5432',
    }
}

# Internal uses the mqtt service built and hosted inside our docker-compose network
MQTT = {
    'internal': {
        'HOST': 'mqtt',
        'PORT': 8000,
        'USER': 'team2',
        'PASSWORD': 'team2',
    }
}

# List of webcameras and their endpoints
# The src field is used in the videostream service
# The api_url is used for the frontend
CAMS = {
    'cam1': {
        "id": "0",
        "src": "http://188.178.124.160:80/mjpg/video.mjpg",
        "api_url": 'http://elab.ase.au.dk/videostream/vstream-direct/test-stand/0',
        "caption": "Et sted i Danmark...",
        "api_activate": 'http://elab.ase.au.dk/videostream/install-test-stand/0'
    },

    'cam2': {
        "id": "1",
        "src": "http://soemon-cho.miemasu.net:63107/nphMotionJpeg?Resolution=640x480&Quality=Motion",
        "api_url": 'http://elab.ase.au.dk/videostream/vstream-direct/test-stand/1',
        "caption": "Et sted i Østen...",
        "api_activate": 'http://elab.ase.au.dk/videostream/install-test-stand/1'
    }
}

# Subscribed topics for the message handler
# It will subscribe to everything in this list
MESSAGE_SUBSCRIPTIONS = [
    ("Testdevice/demo_module/Inbound", 2),
]

# List of inbound handlers (callback functions for each registered module.
# These callback functions must be present in the MODULE.models.py file.
# If they are renamed, change the name here
MESSAGE_CALLBACKS = {
    'demo_module': {
        'status_callback': 'save_incoming_status',
        'data_callback': 'save_incoming_data',
        'fallback_callback': 'save_failed_validation'
    },
}

# get the xth part of the topic, e.g. Testdevice/accelerometer/outbound.
# Element 1 is accelerometer
GET_TOPIC_COMPONENT = 1


# Path for the protocol schema
PROTOCOL_SCHEMA_NAME = "protocol_v1_1.schema"
PROTOCOL_SCHEMA_PATH = os.path.join(
    BASE_DIR, "webinterface", PROTOCOL_SCHEMA_NAME)

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [("assets", '/var/www/static/'),
                    ]
