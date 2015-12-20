# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from easy_thumbnails.conf import Settings as ThumbnailSettings


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v!hoc*um31g14-$w%@cy%=(o&-&qxk32sc2gl)!ukmv84+f(_6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'flat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # MPTTModel and Tree views in django admin
    'mptt',
    'django_mptt_admin',

    # Ckeditor
    'ckeditor_uploader',
    'ckeditor',


    # Thumbnails engine
    'easy_thumbnails',
    'image_cropping',

    # Chained selects
    'smart_selects',

    # Admin reorder feature
    'admin_reorder',

    # Import-Export
    'import_export',

    # APPS
    'website',
    'webshop',
    'weblayout',
    'webshopcart',
    'webrating'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
    'django.middleware.gzip.GZipMiddleware',
)

ADMIN_REORDER = (
    'auth',

    {'app': 'weblayout', 'label': 'Web Site General Settings', 'models': (
        {'model': 'weblayout.MainMenu', 'label': 'Main Menu Constructor'},
        {'model': 'weblayout.ExtraMenu', 'label': 'Extra Menu Constructor'},
        {'model': 'weblayout.AdditionalMenu', 'label': 'Additional Menu Constructor'},
        {'model': 'weblayout.SystemElement', 'label': 'System Elements Manager'},
        {'model': 'weblayout.Template', 'label': 'Manage Templates (Service Staff Only!)'},
        {'model': 'weblayout.Language', 'label': 'Manage Language'},
    )},

    {'app': 'website', 'label': 'Web Site', 'models': (
        {'model': 'website.StaticPage', 'label': 'Static Pages Manager'},
        {'model': 'website.Gallery', 'label': 'Galleries Manager'},
        {'model': 'website.Banner', 'label': 'Banners Manager'},
        {'model': 'website.BannerImagePosition', 'label': 'Manage Banners Images'},
        {'model': 'website.GalleryImagePosition', 'label': 'Manage Galleries Images'},
    )},

    {'app': 'webshop', 'label': 'Web Shop', 'models': (
        {'model': 'webshop.Category', 'label': 'Manage Categories'},
        {'model': 'webshop.Product', 'label': 'Manage Products'},
        {'model': 'webshop.PreFilter', 'label': 'PreFilters'},
        {'model': 'webshop.Currency', 'label': 'Manage Currencies'},
        {'model': 'webshop.Provider', 'label': 'Manage Providers'},
        {'model': 'webshop.SpecialProposition', 'label': 'Manage Special Propositions'},
        {'model': 'webshop.ProductParameterCollection', 'label': 'Products Parameters Collections'},
        {'model': 'webshop.ProductParameter', 'label': 'Manage Available Product Parameters'},
        {'model': 'webshop.ProductParameterAvailableValue', 'label': 'Manage Product Parameters Available Values'},
        {'model': 'webshop.ProductImagePosition', 'label': 'Manage Products Images'},
        {'model': 'webshop.ProductParameterValue', 'label': 'Products Parameters'},
        {'model': 'webshop.Sale', 'label': 'Products Sales'},
        {'model': 'webshop.Margin', 'label': 'Products Margins'},
        {'model': 'webshop.DeliveryRule', 'label': 'Delivery Rules'}

    )},

    {'app': 'webshopcart', 'label': 'Cart', 'models': (
        {'model': 'webshopcart.ProductInCart', 'label': 'Products in Cart'},
        {'model': 'webshopcart.ProductCart', 'label': 'Cart'},
    )},

    {'app': 'webrating', 'label': 'Ratings and comments', 'models': (
        {'model': 'webrating.Rating', 'label': 'Ratings'},
    )},
)

ROOT_URLCONF = 'frankie_web_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates/'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'frankie_web_platform.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3'
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

# Uncomment this line to test custom static files in developer mode
STATICFILES_DIRS = ('static',)

# STATIC_ROOT = 'static'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SESSION_SAVE_EVERY_REQUEST = True

COMPRESS_HTML = False

CKEDITOR_UPLOAD_PATH = "uploads"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Undo', 'Redo',
             '-', 'Bold', 'Italic', 'Underline',
             '-', 'Link', 'Unlink', 'Anchor',
             '-', 'Format',
             '-', 'Maximize',
             '-', 'Table',
             '-', 'Image',
             '-', 'Source',
             '-', 'NumberedList', 'BulletedList'
             ],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
             '-', 'Font', 'FontSize', 'TextColor',
             '-', 'Outdent', 'Indent',
             '-', 'HorizontalRule',
             '-', 'Blockquote'
             ]
        ],
        'height': 500,
        'width': '100%',
        'toolbarCanCollapse': False,
        'forcePasteAsPlainText': True,
        'allowedContent': True,
        'filebrowserBrowseUrl': '/ckeditor/browse/',
        'filebrowserUploadUrl': '/ckeditor/upload/'
    }
}
USE_DJANGO_JQUERY = True
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'

GALLERY_IMAGE_LARGE = '1200x800'
GALLERY_IMAGE_MEDIUM = '750x230'
GALLERY_IMAGE_SMALL = '62x44'

PRODUCT_IMAGE_LARGE = '960x680'
PRODUCT_IMAGE_MEDIUM = '162x122'
PRODUCT_IMAGE_SMALL = '62x44'

SIMILAR_PRODUCTS_NUM = 1

PRODUCT_ON_PAGE = 9

THUMBNAIL_PROCESSORS = ('image_cropping.thumbnail_processors.crop_corners',) + ThumbnailSettings.THUMBNAIL_PROCESSORS

