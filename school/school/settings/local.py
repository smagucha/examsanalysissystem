from .base import *

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = []

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": config("ENGINE"),
        "NAME": config("NAME"),
        "USER": config("USER"),
        "PASSWORD": config("PASSWORD"),
        "HOST": config("HOST"),
        "PORT": config("PORT"),
    }
}
