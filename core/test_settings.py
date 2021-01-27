from .settings import *  # NOQA

ALLOWED_HOSTS = ["*"]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
