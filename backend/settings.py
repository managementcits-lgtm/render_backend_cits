from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".onrender.com"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "api",
]

MIDDLEWARE = [
     "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"
WSGI_APPLICATION = "backend.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASE_URL = os.environ.get("DATABASE_URL")
RENDER = os.environ.get("RENDER")  

if RENDER and DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAdminUser",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    ),
}



#tel

TELEGRAM_CAREER_BOT_TOKEN = os.environ.get("TELEGRAM_CAREER_BOT_TOKEN")
TELEGRAM_CAREER_CHAT_ID = os.environ.get("TELEGRAM_CAREER_CHAT_ID")

TELEGRAM_CONTACT_BOT_TOKEN = os.environ.get("TELEGRAM_CONTACT_BOT_TOKEN")
TELEGRAM_CONTACT_CHAT_ID = os.environ.get("TELEGRAM_CONTACT_CHAT_ID")

TELEGRAM_CPU_BOT_TOKEN = os.environ.get("TELEGRAM_CPU_BOT_TOKEN")
TELEGRAM_CPU_CHAT_ID = os.environ.get("TELEGRAM_CPU_CHAT_ID")

TELEGRAM_HACKATHON_TOKEN = os.environ.get("TELEGRAM_HACKATHON_TOKEN")
TELEGRAM_HACKATHON_ID = os.environ.get("TELEGRAM_HACKATHON_ID")


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://cits.org.in",
    "https://www.cits.org.in",
]

CORS_ALLOW_CREDENTIALS = True

#hosts
ALLOWED_HOSTS = [
    "api.cits.org.in",
    "cits.org.in",
    "www.cits.org.in",
    ".onrender.com",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
