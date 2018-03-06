from mysite.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ra=(v+)xn!!a6uqu*%7a$tkrq$77fu)0s9uj-)ojtt_f1@8vn9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'mysite',
        'USER': 'frankie',
        'PASSWORD': 'gofrankie8$',
    }
}
