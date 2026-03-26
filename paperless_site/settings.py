import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i%cnh7g@tejy5$&y1v2#i!r(nj&k$13zs9=w_ed5we491juopc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['tyrell-choicest-michell.ngrok-free.dev', 'localhost', '127.0.0.1', '*']

# Payagan ang pag-embed ng iframe (Kailangan para sa Modal Preview)
X_FRAME_OPTIONS = 'ALLOWALL'

# Opsyonal: Para sa mas smooth na connection sa Ngrok
CSRF_TRUSTED_ORIGINS = ['https://tyrell-choicest-michell.ngrok-free.dev']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tracking',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'paperless_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'tracking.context_processors.global_counts', 
            ],
        },
    },
]

WSGI_APPLICATION = 'paperless_site.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_paperless',  
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3307',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

# ==========================================
# STATIC AND MEDIA FILES CONFIGURATION
# ==========================================

STATIC_URL = 'static/'

# Dito nagkaroon ng conflict base sa screenshot mo.
# Siguraduhin nating kasama ang 'static' folder sa root ng project.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Path para sa in-upload na mga dokumento
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Gagamitin ito kapag nag-python manage.py collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ==========================================
# AUTHENTICATION PATHS
# ==========================================

LOGIN_URL = 'login' 
LOGIN_REDIRECT_URL = 'user_dashboard'
LOGOUT_REDIRECT_URL = 'login'

# ==========================================
# EMAIL CONFIGURATION (GMAIL SMTP)
# ==========================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'marvindelluza99@gmail.com'  
EMAIL_HOST_PASSWORD = 'fsyevtvhhksiqwrd' 
DEFAULT_FROM_EMAIL = 'ERDM System <marvindelluza99@gmail.com>'