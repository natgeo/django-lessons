from django.conf import settings
from django.db.models import Q
from django.template.defaultfilters import slugify


DEFAULT_SETTINGS = {
    'RELATION_MODELS': [],
    'KEY_IMAGE': None,
    'RESOURCE_CAROUSEL': None,
    'RC_SLIDE': None,
    'ASSESSMENT_TYPES': (
        ('alternative', 'Alternative Assessment'),
        ('authentic', 'Authentic Assessment'),
        ('formative', 'Formative Assessment'),
        ('informal', 'Informal Assessment'),
        ('observation', 'Observation'),
        ('peer-evaluation', 'Peer Evaluation'),
        ('portfolio', 'Portfolio Assessment'),
        ('rubric', 'Rubric'),
        ('self', 'Self Assessment'),
        ('standardized', 'Standardized Testing'),
        ('testing', 'Testing'),
    ),
    'INTERNET_ACCESS_TYPES': (
        (1, 'No'),
        (2, 'Optional'),
        (3, 'Required'),
    ),
    'PEDAGOGICAL_PURPOSE_TYPE_CHOICES': (
        (1, 'apply'),
        (2, 'develop'),
        (3, 'engage'),
    ),
    'STANDARD_TYPES': (
        (1, 'Energy Literacy Essential Principles and Fundamental Concepts'),
        (2, 'IRA/NCTE Standards for the English Language Arts'),
        (4, 'National Council for Social Studies Curriculum Standards'),
        (5, 'National Geography Standards'),
        (6, 'National Science Education Standards'),
        (7, 'National Standards for Arts Education'),
        (8, 'National Standards for History'),
        (3, 'NCTM Principles and Standards for School Mathematics'),
        (9, 'Ocean Literacy Essential Principles and Fundamental Concepts'),
        (10, 'TEST: State Standards'),
        (11, 'Voluntary National Content Standards in Economics'),
        (12, 'Common Core State Standards for English Language Arts & Literacy'),
        (13, 'Common Core State Standards for Mathematics'),
    ),
    'STANDARD_TYPE_SLUGS': {},  # key => slug
    'JAVASCRIPT_URL': settings.MEDIA_URL + 'js/',
    'CREDIT_MODEL': None,
    'GLOSSARY_MODEL': None,
    'RCS_MODEL': None,
    'RESOURCE_MODEL': None,
    'REPORTING_MODEL': None,
}

DEFAULT_SETTINGS.update(getattr(settings, 'LESSON_SETTINGS', {}))

# if DEFAULT_SETTINGS['KEY_IMAGE'] is None:
#     raise ImproperlyConfigured("The KEY_IMAGE setting for curricula is not set.")

globals().update(DEFAULT_SETTINGS)

## Create a mapping from a key to a dict of name and slug
STD_TYPE_KEY_MAP = dict([
    (key, {'name': val, 'slug': slugify(val)}) for key, val in STANDARD_TYPES
])
for key, val in STANDARD_TYPE_SLUGS:
    STD_TYPE_KEY_MAP[key]['slug'] = val

## Create a mapping from a slug to a dict of name and key
STD_TYPE_SLUG_MAP = dict([
    (val['slug'], {'name': val['name'], 'key': key}) for key, val in STD_TYPE_KEY_MAP.items()
])
RELATIONS = [Q(app_label=al, model=m) for al, m in [x.split('.') for x in RELATION_MODELS]]
