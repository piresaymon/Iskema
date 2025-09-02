# Arquivo: iskema/settings.py

import os
# Substitui dj_database_url (opcional, mas recomendado atualizar se usar)
# import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Atualiza para o método recomendado no Django 3.1+
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-generated-secret-key-here-change-this' # Gere uma nova!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0'] # Adicione seu domínio em produção


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin', # Descomentado para acesso ao admin (opcional)
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core', # Sua app
    # Adicione outras apps aqui se necessário
]

# Atualiza MIDDLEWARE_CLASSES para MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware', # Pode ser comentado se @csrf_exempt for usado, mas é recomendado
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'iskema.urls' # Certifique-se de que o nome do projeto está correto

# Atualiza TEMPLATE_DIRS para TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Atualiza DIRS para usar Path e refletir a nova estrutura
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True, # Permite que apps tenham suas próprias pastas de templates
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'iskema.wsgi.application' # Certifique-se de que o nome do projeto está correto


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Exemplo para SQLite (padrão para desenvolvimento)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Se quiser usar dj_database_url com uma versão atualizada:
# DATABASES = {
#     'default': dj_database_url.config(
#         default='sqlite:///db.sqlite3',
#         conn_max_age=600,
#         conn_health_checks=True,
#     )
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br' # Atualizado para português do Brasil

TIME_ZONE = 'America/Sao_Paulo' # Atualizado para o fuso horário de SP

USE_I18N = True

USE_TZ = True # Atualizado para True (recomendado)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
# Atualiza STATIC_ROOT para usar Path
STATIC_ROOT = BASE_DIR / 'staticfiles' # Pasta onde os arquivos são coletados para produção

# Atualiza STATICFILES_DIRS para usar Path
STATICFILES_DIRS = [
    BASE_DIR / 'static', # Pasta de arquivos estáticos locais
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Logging (opcional, mantido do original com pequenas atualizações)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        # 'mail_admins': { # Pode ser removido se não usar
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'include_html': True,
        # }
    },
    'root': {
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        # 'django.request': { # Pode ser ajustado ou removido
        #     'handlers': ['mail_admins'],
        #     'level': 'ERROR',
        #     'propagate': True,
        # },
    },
}
