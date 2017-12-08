from django.conf import settings
import environ


PROJECT_ROOT = environ.Path(__file__) - 2


def pytest_configure():
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'dev.db',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sites',
            'acknowledge',
            'audience',
            'categories',
            'categories.editor',
            'cms',
            'concepts',
            'contentrelations',
            'credits',
            'curricula',
            'edumetadata',
            'licensing',
            'menus',
            'quotations',
            'reference',
            'resource_carousel',
            'taxonomy',
            'treebeard',
        ],
        LANGUAGE_CODE='en-us',
        MEDIA_URL='/uploads/',
        PROJECT_ROOT=PROJECT_ROOT,
        ROOT_URLCONF='curricula.urls',
        SITE_ID=1,
        STATIC_URL='/static/',
        TEMPLATES=[{
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
        USE_TZ=True,
    )
