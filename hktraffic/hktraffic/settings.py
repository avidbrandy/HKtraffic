import os
from configparser import ConfigParser
from django.core.management import utils


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

cfg = ConfigParser()
cfg.read(os.path.join(BASE_DIR, 'config.ini'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = utils.get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = cfg.getboolean('app', 'debug', fallback=False)

ALLOWED_HOSTS = ['localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    
    'hktraffic',
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

#ROOT_URLCONF = 'hktraffic.urls'

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

#WSGI_APPLICATION = 'hktraffic.wsgi.application'

USE_SQLITE_DB = cfg.getboolean('app', 'use_sqlite_db', fallback=False)

if USE_SQLITE_DB:
    db = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
else:
    database = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': cfg.get('database', 'db_name'),
        'USER': cfg.get('database', 'user'),
        'PASSWORD': cfg.get('database', 'password'),
        'HOST': cfg.get('database', 'host'),
        'PORT': cfg.get('database', 'port'),
        'OPTIONS': {'sslmode': 'require'},
    }

DATABASES = {
    'default': database,
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = cfg.get('app', 'static_root', fallback='')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# login for proxies
proxy_username = cfg.get('proxy', 'username')
proxy_password = cfg.get('proxy', 'password')
