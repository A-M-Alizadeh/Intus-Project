"""
Settings for running Django in Docker (e.g. via docker-compose).

By default this keeps SQLite (from base settings) for simplicity.
You can optionally enable PostgreSQL by setting USE_POSTGRES=1.
"""
import os

from .base import *  # noqa: F401, F403

DEBUG = os.getenv("DEBUG", "0").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = (
    os.getenv("ALLOWED_HOSTS", "*").split(",")
    if os.getenv("ALLOWED_HOSTS")
    else [".hf.space", "localhost", "127.0.0.1"]
)

if os.getenv("USE_POSTGRES", "0").lower() in ("1", "true", "yes"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "intus"),
            "USER": os.getenv("POSTGRES_USER", "intus"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
            "HOST": os.getenv("POSTGRES_HOST", "db"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }

# Hugging Face Spaces renders the app in an iframe on huggingface.co.
# Allow framing to avoid "refused to connect" in the Space UI.
X_FRAME_OPTIONS = "ALLOWALL"
