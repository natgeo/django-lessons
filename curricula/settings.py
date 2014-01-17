from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.template.defaultfilters import slugify

DEFAULT_MCE_ATTRS = {
    'plugins': "rawmode,paste",
    'theme_advanced_buttons1': "pasteword,|,bold,underline,italic,strikethrough,|,link,unlink,|,numlist,bullist,|,charmap,|,rawmode",
    'theme_advanced_buttons2': "",
    'entity_encoding': 'numeric',
}

SUBTITLE_MCE_ATTRS = {
    'plugins': "rawmode,paste",
    'theme_advanced_buttons1': "pasteword,|,bold,underline,italic,strikethrough,|,link,unlink,|,numlist,bullist,|,charmap,|,rawmode",
    'theme_advanced_buttons2': "",
    'height': "150",
    'entity_encoding': 'numeric',
}

DIRECTIONS_MCE_ATTRS = {
    'content_css': settings.STATIC_URL + "css/glossary_term.css",
    'theme_advanced_buttons1': 'glossify, fullscreen,preview,code,print,spellchecker,|,cut,copy,paste,pastetext,pasteword,undo,redo,|,search,replace,|,rawmode',
    'setup': 'add_button_callback',
    'entity_encoding': 'numeric',
}

DEFAULT_SETTINGS = {
    'RELATION_MODELS': [],
    'KEY_IMAGE': None,  # ('field_name', 'applabel.model')
    'RESOURCE_CAROUSEL': None,
    'RC_SLIDE': None,
    'ASSESSMENT_TYPES': (
        ('alternative', 'Alternative Assessment'),
        ('authentic', 'Authentic Assessment'),
        ('formal', 'Formal Assessment'),
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
        (4, 'assess'),
        (2, 'develop'),
        (3, 'engage'),
        (5, 'inquiry'),
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
    'GLOSSARY_MODEL': 'reference.GlossaryTerm',
    'RESOURCE_MODEL': 'resource_carousel.ExternalResource',
    'REPORTING_MODEL': None,
    'DEFAULT_LICENSE': 23,
    'RELATION_TYPES': None,
    'TIP_TYPE_CHOICES': (
        (1, 'Tip'),
        (2, 'Modification'),
    ),
    'MCE_ATTRS': None,
    'REQUIRE_REPORTING_CATEGORIES': True,
}

DEFAULT_SETTINGS.update(getattr(settings, 'LESSON_SETTINGS', {}))

# if DEFAULT_SETTINGS['KEY_IMAGE'] is None:
#     raise ImproperlyConfigured("The KEY_IMAGE setting for curricula is not set.")
if DEFAULT_SETTINGS['MCE_ATTRS']:
    if isinstance(DEFAULT_SETTINGS['MCE_ATTRS'], dict):
        if not isinstance(DEFAULT_SETTINGS['MCE_ATTRS'].values()[0], dict):
            # If the values aren't a dict, then they passed in a TinyMCE config
            # for all fields. Convert it to {'default': }
            DEFAULT_SETTINGS['MCE_ATTRS'] = {'default': DEFAULT_SETTINGS['MCE_ATTRS'].copy()}
        elif 'default' not in DEFAULT_SETTINGS['MCE_ATTRS']:
            DEFAULT_SETTINGS['MCE_ATTRS']['default'] = DEFAULT_MCE_ATTRS
    else:
        raise ImproperlyConfigured("The MCE_ATTRS setting must be either a dict containing one TinyMCE configuration or a dict formatted as {'field': tinymce_dict}")
else:
    DEFAULT_SETTINGS['MCE_ATTRS'] = {
        'default': DEFAULT_MCE_ATTRS,
        'subtitle_guiding_question': SUBTITLE_MCE_ATTRS,
        'directions': DIRECTIONS_MCE_ATTRS
    }

TINYMCE_FIELDS = ('description', 'assessment', 'learning_objectives',
                  'other_notes', 'background_information')
ACTIVITY_TINYMCE_FIELDS = TINYMCE_FIELDS + ('directions',
                'subtitle_guiding_question', 'extending_the_learning',
                'setup', 'accessibility_notes', 'prior_knowledge')
IDEACATEGORY_TINYMCE_FIELDS = ('content_body', 'description')
LESSON_TINYMCE_FIELDS = TINYMCE_FIELDS + ('subtitle_guiding_question', 'prior_knowledge')
UNIT_TINYMCE_FIELDS = TINYMCE_FIELDS + ('subtitle', 'overview')

globals().update(DEFAULT_SETTINGS)

ACTIVITY_FIELDS = []
LESSON_FIELDS = []
if DEFAULT_SETTINGS['KEY_IMAGE'] is not None:
    ACTIVITY_FIELDS.append(DEFAULT_SETTINGS['KEY_IMAGE'])
    LESSON_FIELDS.append(DEFAULT_SETTINGS['KEY_IMAGE'])

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
