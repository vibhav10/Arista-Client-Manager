from .base_settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
         'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'


# # CSRF SETTINGS
#CSRF_TRUSTED_ORIGINS = ['https://*', 'http://*']
CSRF_TRUSTED_ORIGINS = ['https://d28f-115-112-36-43.ngrok-free.app']

# # CORS SETTINGS
CORS_ORIGIN_ALLOW_ALL = True
