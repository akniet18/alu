"""
Django settings for alu project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3j6@k*55+qzyl#)g_d)hdpk0hehe@buv5%6hiuo^nhzzx$!rmx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users',
    'categories',
    'products',
    'locations',
    'basket',
    'message',

    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'huey.contrib.djhuey',
    "push_notifications"
    # 'django_celery_beat',
    # 'django_celery_results',
    # 'django_cron',
    # 'django_crontab',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

APPEND_SLASH=False
ROOT_URLCONF = 'alu.urls'
AUTH_USER_MODEL = 'users.User'

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

WSGI_APPLICATION = 'alu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'alu',
        'USER': 'postgres',
        'PASSWORD': 'pwd123',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 0,
    }
}


PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": "AAAAdP7JCPQ:APA91bGdRe148TLzC2QZO_d_RJVrfgxw21jQ7Na0kderD-_C9DCBUi0Gmxt3OLKEp4Vcyb-KaJeNiefcjR-nQBotnwE-hLzsuyylqviFEGJpQ-taez6IATI_df6SZ3_TD6rgi39N_czr",
    "APNS_CERTIFICATE": "var/www/aluonline/aps.pem",
    "APNS_TOPIC": "com.kz.ALU",
    "WNS_PACKAGE_SECURITY_ID": "[your package security id, e.g: 'ms-app://e-3-4-6234...']",
    "WNS_SECRET_KEY": "[your app secret key, e.g.: 'KDiejnLKDUWodsjmewuSZkk']",
    "WP_PRIVATE_KEY": "/path/to/your/private.pem",
    "WP_CLAIMS": {'sub': "mailto: development@example.com"}
}


HUEY = {
    'huey_class': 'huey.RedisHuey',  # Huey implementation to use.
    'name': DATABASES['default']['NAME'],  # Use db name for huey.
    'results': True,  # Store return values of tasks.
    'store_none': False,  # If a task returns None, do not save to results.
    'immediate': False,  # If DEBUG=True, run synchronously.
    'utc': True,  # Use UTC for all times internally.
    'blocking': True,  # Perform blocking pop rather than poll Redis.
    'connection': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'connection_pool': None,  # Definitely you should use pooling!
        # ... tons of other options, see redis-py for details.

        # huey-specific connection parameters.
        'read_timeout': 1,  # If not polling (blocking pop), use timeout.
        'url': None,  # Allow Redis config via a DSN.
    },
    'consumer': {
        'workers': 1,
        'worker_type': 'thread',
        'initial_delay': 0.1,  # Smallest polling interval, same as -d.
        'backoff': 1.15,  # Exponential backoff using this rate, -b.
        'max_delay': 10.0,  # Max possible polling interval, -m.
        'scheduler_interval': 1,  # Check schedule every second, -s.
        'periodic': True,  # Enable crontab feature.
        'check_worker_health': True,  # Enable worker health checks.
        'health_check_interval': 1,  # Check worker health every second.
    },
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# If time zones are active (USE_TZ = True) define your local 
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_TIMEZONE = 'Asia/Almaty'
# app.conf.enable_utc = False # so celery doesn't take utc by default
# We're going to have our tasks rolling soon, so that will be handy 
# from celery.task.schedules import crontab

# CELERY_BEAT_SCHEDULE = {
#     'send-notification': { 
#         'task': 'basket.tasks.send_notification', 
#         'schedule': 10,
#     },          
# }


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DATETIME_FORMAT': "%d.%m.%Y %H:%M:%S",
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')