from .base import *

ALLOWED_HOSTS = [
    "127.0.0.1:8000",
    "https://school-exam-analysis-system.uc.r.appspot.com",
]
SECRET_KEY = env("SECRET_KEY")
