import datetime

from .settings import *  # noqa

# Time duration for weather checker application
CURRENT_DURATION = datetime.timedelta(seconds=10)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "$)bxhkmx(2fv92*%c)^%k^v#o!3=_g_am%*@9rg651!z)&6kjg"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]
