from .base import *

DEBUG = env("DEBUG", cast=bool)
ALLOWED_HOSTS = ["*"]

SECRET_KEY = env("SECRET_KEY")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
