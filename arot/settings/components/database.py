import os
from decouple import config
from arot.settings.paths import BASE_DIR

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
POSTGRESQL = config('POSTGRESQL', cast=bool, default=False)

if POSTGRESQL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', cast=str),
            'USER': config('DB_USER', cast=str),
            'PASSWORD': config('DB_PASSWORD', cast=str),
            'HOST': config('DB_HOST', cast=str),
            'PORT': config('DB_PORT', cast=str),
            'TEST': {
                'NAME': config('TEST_DB_NAME', 'arottest'),
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
