# Django settings for example project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
import os
import sys

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
APP = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(APP)

ADMINS = (
    ('Rajit K Sarkar', 'rsarkar@celerity.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'dev.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(ROOT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# required by django-concepts
STATIC_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'g2_39yupn*6j4p*cg2%w643jiq-1n_annua*%i8+rq0dx9p=$n'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
  # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'example.urls'

TEMPLATE_DIRS = (
    "%s/%s/" % (ROOT_PATH, 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    # 'django.contrib.messages',
    # 'south',
    'tinymce',
    'categories',
    'categories.editor',
    'concepts',
    'edumetadata',
    # 'reversion',
    # 'publisher',
    'curricula',
    'audience',
    'dummy',
)

TINYMCE_JS_URL = "%sjs/tiny_mce/tiny_mce_src.js" % MEDIA_URL

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'plugins': "safari,spellchecker,pagebreak,advimage,advlink,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,directionality,fullscreen,noneditable,nonbreaking,xhtmlxtras",
    'theme_advanced_buttons3_add': "|,spellchecker",
    'theme_advanced_buttons1': "fullscreen,preview,code,print,spellchecker,|,cut,copy,paste,pastetext,pasteword,undo,redo,|,search,replace,|,rawmode",
    'theme_advanced_buttons2': "formatselect,fontselect,fontsizeselect,insertfile,insertimage,|,bold,underline,italic,strikethrough,|,link,unlink,|,numlist,bullist,|,sub,sup,charmap,insertdate,inserttime,|,outdent,indent,|,justifyleft,justifycenter,justifyright,justifyfull,|,ltr,rtl,|,backcolor,forecolor,pagebreak",
    'theme_advanced_buttons3': "",
    'theme_advanced_disable': 'cut,copy,paste,cite,abbr,acronym,fontselect,fontsizeselect,forecolor,backcolor,forecolorpicker,backcolorpicker,blockquote,del,ins',
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_toolbar_align': "left",
    'theme_advanced_statusbar_location': "bottom",
    'theme_advanced_resizing': "true",
    'theme_advanced_resize_horizontal': 1,
    'theme_advanced_resizing_max_width': "750",
    'width': "750",
    'height': "250",
    'entity_encoding': 'raw',
}

TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = False
TINYMCE_FILEBROWSER = False

LESSON_SETTINGS = {
    'RELATION_MODELS': (
        'dummy.promo',
      # 'lessons.activity', # for use as model student work, picture of practice
    ),
    'ACTIVITY_FIELDS': (
        ('resource_carousel', 'dummy.resourcecarousel'),
        ('key_image', 'dummy.photo'),
    ),
    'REQUIRED_FIELDS': (
        ('resource_carousel', 'dummy.resourcecarousel'),
        ('key_image', 'dummy.photo'),
    ),
}

# CATEGORIES_SETTINGS = {
#     'FK_REGISTRY': {'curricula.Lesson': (
#         {'name': 'primary_category', 'related_name': 'primary_cat', 'blank': True, 'null': True},
#     )},
#     'M2M_REGISTRY': {'curricula.Lesson': (
#         {'name': 'secondary_categories', 'blank': True, 'null': True},
#     )}
# }

CONCEPTS_SETTINGS = {
    'WEIGHTS': ((0, 'Hide'), (10, 'Very Low'), (20, 'Low'), (30, 'Medium'), (40, 'High'), (50, ' Very High')),
}

try:
    from local_settings import *
except ImportError, exp:
    pass
