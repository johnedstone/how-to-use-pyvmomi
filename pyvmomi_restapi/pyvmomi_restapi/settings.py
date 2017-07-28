import hashlib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
     hashlib.sha1(os.urandom(128)).hexdigest(), 
)

DEBUG = os.environ.get('DEBUG', 'on') == 'on'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost 127.0.0.1').split()

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    # Third party apps
    'rest_framework',
    'rest_framework_swagger',
    'corsheaders',

    # Internal apps
    'vm_helpers',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pyvmomi_restapi.urls'

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

WSGI_APPLICATION = 'wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] [%(name)s.%(module)s.%(funcName)s:%(lineno)d] %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console_verbose': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'info_verbose': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'console_verbose_prod': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'develop_logger': {
            'handlers': ['console_verbose'],
            'level': 'INFO',
            'filters': ['require_debug_true']
        },
        'info_logger': {
            'handlers': ['info_verbose'],
            'level': 'INFO',
        },
        'prod_logger': {
            'handlers': ['console_verbose_prod'],
            'level': 'ERROR',
            'filters': ['require_debug_false']
        },
    }
}

if DEBUG:
    PROJECT_LOGGING = 'develop_logger'
else:
    PROJECT_LOGGING = 'info_logger'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

CORS_ORIGIN_ALLOW_ALL = True

# Disable browsable API in production
if not DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
                'rest_framework.renderers.JSONRenderer',)

# For using SSL with openshift
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATE_CHOICES = (
    ('mount', 'mount'),
    ('umount', 'umount'),
)

VSPHERE_USERNAME = os.environ.get('VSPHERE_USERNAME', 'giberish_user')
VSPHERE_PASSWORD = os.environ.get('VSPHERE_PASSWORD', 'giberish_password')

SWAGGER_SETTINGS = {
    'VALIDATOR_URL': None,
}
# vim: ai et ts=4 sw=4 sts=4 nu ru
