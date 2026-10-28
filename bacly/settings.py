import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env
load_dotenv(BASE_DIR / ".env")

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-bacly-default-development-key-2026")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

allowed_hosts_env = os.getenv("ALLOWED_HOSTS", "*")
ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_env.split(",") if h.strip()] or ["*"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # Bacly apps
    "accounts.apps.AccountsConfig",
    "classes.apps.ClassesConfig",
    "core.apps.CoreConfig",
    "tutor.apps.TutorConfig",
    "practice.apps.PracticeConfig",
    "exams.apps.ExamsConfig",
    "progress.apps.ProgressConfig",
]

AUTH_USER_MODEL = "accounts.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bacly.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.global_context",
            ],
        },
    },
]

WSGI_APPLICATION = "bacly.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 4},
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files (for student uploaded math exercise pictures)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Auth redirection
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"

# Iframe & CSRF settings for AI Studio preview environment
X_FRAME_OPTIONS = "ALLOWALL"
CSRF_TRUSTED_ORIGINS = [
    "https://*.run.app",
    "https://*.google.com",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://localhost:8080",
]

# Cookie security: strict SameSite=None + Secure in production (AI Studio is HTTPS),
# relaxed Lax + non-secure for local HTTP development via run_dev.py.
SAMESITE_NONE_SECURE = {
    "SESSION_COOKIE_SAMESITE": "None",
    "SESSION_COOKIE_SECURE": True,
    "CSRF_COOKIE_SAMESITE": "None",
    "CSRF_COOKIE_SECURE": True,
}
LOCAL_DEV_COOKIES = {
    "SESSION_COOKIE_SAMESITE": "Lax",
    "SESSION_COOKIE_SECURE": False,
    "CSRF_COOKIE_SAMESITE": "Lax",
    "CSRF_COOKIE_SECURE": False,
}

cookie_conf = SAMESITE_NONE_SECURE if not DEBUG else LOCAL_DEV_COOKIES
for key, value in cookie_conf.items():
    globals()[key] = value

# AI Provider Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")

# Rate limit configuration: 30 calls per user per hour
AI_RATE_LIMIT_PER_HOUR = 30
