from django.conf import settings
import environ
import os


PROJECT_ROOT = environ.Path(__file__) - 2

env = environ.Env()

if os.path.exists(PROJECT_ROOT('.env')):
    env.read_env(PROJECT_ROOT('.env'))


def pytest_configure():

    settings_kwargs = {
        'DEBUG': True,
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'dev.db',
            }
        },
        'INSTALLED_APPS': [
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sites',
            'acknowledge',
            'audience',
            'biography',
            'categories',
            'categories.editor',
            'cms',
            'concepts',
            'contentrelations',
            'core_content',
            'core_media',
            'credits',
            'curricula',
            'edumetadata',
            'expeditions',
            'licensing',
            'menus',
            'navigation',
            'ngsprojects',
            'quotations',
            'reference',
            'resource_carousel',
            'sf_models',
            'taxonomy',
            'teachingatlas',
            'treebeard',
            'treenav',
            'viddler',
            'viewmaster',
        ],
        'LANGUAGE_CODE': 'en-us',
        'LESSON_SETTINGS': {
            'RELATION_MODELS': (
                'reference.genericarticle',
                'promotions.tease',
                'promotions.promotion',
                'curricula.activity',  # for use as model student work, picture of practice
                'acknowledge.organization',
                'core_media.ngphoto',
                'interactive_learning.interactive',
            ),
        },
        'MEDIA_URL': '/uploads/',
        'PROJECT_ROOT': PROJECT_ROOT,
        'ROOT_URLCONF': 'curricula.urls',
        'SITE_ID': 1,
        'STATIC_URL': '/static/',
        'TEMPLATES': [{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    "django.contrib.auth.context_processors.auth",
                    "django.template.context_processors.debug",
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.media",
                    "django.template.context_processors.static",
                    "django.template.context_processors.tz",
                    "django.template.context_processors.request",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        }, ],
        'USE_TZ': True,
        'VIDDLER_SETTINGS': {
            'API_KEY': '15z0p5aul5vbiheho0js',
            'USERNAME': 'apiuser',
            'PASSWORD': 'casebook-ave-roll',
        },
    }

    if 'TEST_DATABASE_SERVER' in os.environ:
        TEST_DATABASE_URL = env('TEST_DATABASE_SERVER').rstrip('/') + "/test_curricula"
        DATABASES = {
            'default': env.db_url_config(TEST_DATABASE_URL)
        }
        DATABASES['default']['TEST'] = env.db_url_config(TEST_DATABASE_URL)
    else:
        DATABASES = {
            'default': env.db('TEST_DATABASE_URL', default="postgresql://postgres:@localhost:5432/test_curricula")
        }
        DATABASES['default']['TEST'] = env.db('TEST_DATABASE_URL', default="postgresql://postgres:@localhost:5432/test_curricula")

    settings_kwargs['DATABASES'] = DATABASES

    settings.configure(**settings_kwargs)
