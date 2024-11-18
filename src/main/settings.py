from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ig!$2g6&_*lgs6!8hiihm5yio%z96r=sby(=s9!$kq26%0vopy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # django-allauth
    'django.contrib.sites',    
    'allauth',     
    'allauth.account',     
    'allauth.socialaccount',
    # django-crispy-forms
    "crispy_forms",
    # bootstrap4
    'bootstrap4',
    'bootstrap_datepicker_plus',
    # django-filter
    'django_filters',
    # apps
    'nippo',
    'accounts',
]

# accountsのUserをユーザー認証クラスに設定
AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware", 
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins':[ 
                'bootstrap4.templatetags.bootstrap4',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static_local" ]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media_local"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-allauthの設定
AUTHENTICATION_BACKENDS = [ 
    'django.contrib.auth.backends.ModelBackend',     
    'allauth.account.auth_backends.AuthenticationBackend',
] 

SITE_ID = 1

# ログイン方法をEメール認証へ変更
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False 
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True

# ログイン、ログアウトのリダイレクト先
from django.urls import reverse_lazy
LOGIN_REDIRECT_URL = reverse_lazy('nippo-list')
ACCOUNT_LOGOUT_REDIRECT_URL = reverse_lazy("account_login")

ACCOUNT_ADAPTER = "accounts.adapter.MyNippoAdapter"     # adapter.pyで設定

# emailでの確認を必須
ACCOUNT_EMAIL_VERIFICATION = "mandatory"    # 確認済みじゃない人はログインできない

# ログアウト機能(accounts/logout/へのアクセスでログアウトする)
ACCOUNT_LOGOUT_ON_GET = True

# ターミナルにユーザー登録時のメールを表示
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# django-crispy-forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# bootstrapでjqueryを追加
BOOTSTRAP4 = {
    'include_jquery': True,
}