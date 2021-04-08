from pathlib import Path
import django_heroku
import dj_database_url
from decouple import config
import logging
import os


DATABASES = { 'default': dj_database_url.config(conn_max_age=600, ssl_require=True) }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config('SECRET_KEY') 



# Application definition
INSTALLED_APPS = [
     
    # Third Party app
    'admin_shortcuts',
    'mptt',
    'django_filters',
    'crispy_forms',
    'social_django',
    # 'debug_toolbar',
    'star_ratings',
    'qr_code',

    # rest_frameword app
    'rest_framework',
    'rest_framework.authtoken',
     
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'blog.apps.BlogConfig',
    'shop.apps.ShopConfig',
    'cart.apps.CartConfig',
    'checkout.apps.CheckoutConfig',
    'users.apps.UsersConfig',

    'django_cleanup.apps.CleanupConfig',
    'notifications.apps.NotificationsConfig',

]


ROOT_URLCONF = 'Project.urls'
WSGI_APPLICATION = 'Project.wsgi.application'
INTERNAL_IPS = ['127.0.0.1',]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['*'] # list of domains name


# HTTPS settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# HSTS settings
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True


# Third pary app settings
STAR_RATINGS_RERATE = True
DJANGO_NOTIFICATIONS_CONFIG = { 'USE_JSONFIELD': True}
DJANGO_NOTIFICATIONS_CONFIG = { 'SOFT_DELETE': True}
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
#STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# login redirect url
LOGIN_URL = 'users:users-login'
LOGIN_REDIRECT_URL = 'blog:blog-home'


# Reset password email backend setting
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mohammadfayaj36@gmail.com'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'debug_toolbar.middleware.DebugToolbarMiddleware', #debug_toolbar
    'social_django.middleware.SocialAuthExceptionMiddleware',#social_auth

    'whitenoise.middleware.WhiteNoiseMiddleware',


]


TEMPLATES = [
    {   
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends', #social_auth
                'social_django.context_processors.login_redirect', #social_auth
                
            ],
             'debug': DEBUG,

        },
    },
]



#rest_framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

#DATABASES = {
   # 'default': {
        #'ENGINE': 'django.db.backends.mysql',
        #'NAME': 'eshop',
        #'USER': config('USER'),
        #'PASSWORD': config('PASSWORD'),
        #'HOST': 'localhost',
        #'PORT': '3306',
    #}
#}


# Password validation
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


ADMIN_SHORTCUTS = [
        {
        # 'title': 'Site settings',
        'shortcuts': [

            {
                'title': 'user',
                'url': '/admin/auth/user/',
                'has_perms': 'example.utils.has_perms_to_users',
            },

            {
                'title': 'Customer Address',
                'url': '/admin/users/address/',
                'icon' : 'address-card',
            },

            {
                'title': 'Order',
                'url': '/admin/cart/order/',
                # 'count': 'cart.order.orders',
            },

            {
                'title': 'Product Item',
                'url': '/admin/shop/productitem/',
                
            },


            {
                'title': 'Create Blog Post',
                'url': '/admin/blog/blogpost/',
            },

            {
                'title': 'Change Banner Image',
                'url': '/admin/blog/bannerimage/',
            },

            {
                'title': 'Send Notification',
                'url': '/admin/notifications/notification/',
            },

            {
                'title': 'Change Delivery Charge',
                'url': '/admin/users/deliverycharges/',
                'icon': 'truck',

            },


        ]
    },


]


# ========== SOCIAL_AUTH =============
AUTHENTICATION_BACKENDS = (

    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',


    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    # 'auth_pipelines.pipelines.get_user_avatar',
    
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'

# google 
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')


#twitter
SOCIAL_AUTH_TWITTER_KEY = config('SOCIAL_AUTH_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = config('SOCIAL_AUTH_TWITTER_SECRET')


#facebook
SOCIAL_AUTH_FACEBOOK_KEY = config('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = config('SOCIAL_AUTH_FACEBOOK_SECRET')


SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_link'] 
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {       
  'fields': 'id, name, email, picture.type(large), link'
}

SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [
    ('name', 'name'),
    ('email', 'email'),
    ('picture', 'picture'),
    ('link', 'profile_url'),
]

django_heroku.settings(locals())
