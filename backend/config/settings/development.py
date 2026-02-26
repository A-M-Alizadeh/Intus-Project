from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

try:
    import django_extensions  # noqa: F401
    INSTALLED_APPS = [*INSTALLED_APPS, "django_extensions"]  # noqa: F405
except ImportError:
    pass
