from .base import *

SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)
DATABASES = {
    "default": {
        "ENGINE": config("ENGINE"),
        "HOST": config("HOST"),
        "PORT": config("PORT"),
        "NAME": config("NAME"),
        "USER": config("USER"),
        "PASSWORD": config("PASSWORD"),
    }
}
EMAIL_BACKEND = config("EMAIL_BACKEND")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
ALLOWED_HOSTS = []
TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = config("TWILIO_PHONE_NUMBER")
