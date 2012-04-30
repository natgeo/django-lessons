from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ImproperlyConfigured

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
        (12, 'Common Core State Standards for English Language Arts'),
    ),
    'JAVASCRIPT_URL': settings.MEDIA_URL + 'js/',
    'CREDIT_MODEL': None,
    'REPORTING_MODEL': None,
}

DEFAULT_SETTINGS.update(getattr(settings, 'LESSON_SETTINGS', {}))

# if DEFAULT_SETTINGS['KEY_IMAGE'] is None:
#     raise ImproperlyConfigured("The KEY_IMAGE setting for curricula is not set.")

globals().update(DEFAULT_SETTINGS)

RELATIONS = [Q(app_label=al, model=m) for al, m in [x.split('.') for x in RELATION_MODELS]]
