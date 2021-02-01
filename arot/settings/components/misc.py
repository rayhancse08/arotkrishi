from decouple import config, Csv
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

# GIT_HASH = fetch_git_sha(os.path.dirname(os.pardir))

AdminSite.site_title = ugettext_lazy('Arot Krishi Ponno Ltd. Admin')
AdminSite.site_header = ugettext_lazy('Arot Krishi Ponno Ltd. Administration')
AdminSite.index_title = ugettext_lazy('Arot Krishi Ponno Ltd. ADMINISTRATION')

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
#DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_L10N = True
USE_TZ = True

ROOT_URLCONF = 'arot.urls'
WSGI_APPLICATION = 'arot.wsgi.application'
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost, 127.0.0.1', cast=Csv())
INTERNAL_IPS = config('INTERNAL_IPS', default='127.0.0.1', cast=Csv())
