from pathlib import Path
import os
from dotenv import load_dotenv
import datetime
import logging

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent

# Загрузка переменных окружения из .env файла
load_dotenv()

# Настройки безопасности
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'e2mj4k7r9xgfvzwyuhqbdpci5n3tlsao681f0jesrm2qnxlopyy')
DEBUG = os.getenv("DEBUG", "True").lower() == "true"  # Используем переменную окружения для DEBUG
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1 localhost 192.168.1.2 178.206.254.190").split()

# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'drf_yasg',
    'sections',
    'quiz',
]

# Пользовательская модель
AUTH_USER_MODEL = 'users.User'

# Промежуточное программное обеспечение (Middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS должен быть перед CommonMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',  # Добавляем кэширование
    'django.middleware.cache.FetchFromCacheMiddleware',  # Добавляем кэширование
]

# Основной URL-конфигурационный файл
ROOT_URLCONF = 'config.urls'

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Укажите путь к шаблонам
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,  # Используем значение DEBUG из переменной окружения
        },
    },
]

# WSGI приложение
WSGI_APPLICATION = 'config.wsgi.application'

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'mssql',  # Используем mssql-django для поддержки SQL Server
        'NAME': os.getenv("DJANGO_DATABASE_NAME", "api_eny"),
        'USER': os.getenv('DJANGO_DATABASE_USER'),
        'PASSWORD': os.getenv('DJANGO_DATABASE_PASSWORD'),
        'HOST': os.getenv('DJANGO_DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DJANGO_DATABASE_PORT', ''),
        'OPTIONS': {
            'driver': os.getenv('DJANGO_DATABASE_OPTIONS_DRIVER', 'ODBC Driver 17 for SQL Server'),
            'TrustServerCertificate': 'yes',
            'Encrypt': 'optional',
        },
    }
}

# Язык и часовой пояс
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Статические файлы
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Медиа файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Автоинкрементные поля
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Защита всех эндпоинтов
    ),
}

# Настройки JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),
}

# Настройки CORS
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000 http://127.0.0.1:3000").split()
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "http://localhost:3000 http://127.0.0.1:3000").split()

# Логирование
logger = logging.getLogger(__name__)

# Настройки кэша Redis
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        "LOCATION": os.getenv("CACHE_LOCATION", "redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": False,
            "SOCKET_TIMEOUT": 1,
        }
    }
}

# Проверка подключения к Redis
try:
    from django.core.cache import cache
    cache.get('test_cache_connection')
except Exception as e:
    logger.error(f"Redis connection error: {e}")

# Настройки логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'debug.log',  # Логи теперь хранятся в папке logs
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
        },
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
        },
    },
}

# Настройки кэширования
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() == "true"
CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = ""

# Создаем папку для логов, если она не существует
if not (BASE_DIR / 'logs').exists():
    (BASE_DIR / 'logs').mkdir(parents=True)

# Создаем папку для статических файлов, если она не существует
if not (BASE_DIR / 'static').exists():
    (BASE_DIR / 'static').mkdir(parents=True)
