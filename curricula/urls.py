from django.conf.urls.defaults import *
from .models import Activity, Lesson

urlpatterns = patterns('',
    url(r'objectives/(?P<id>\d+)/$',
        'curricula.views.learning_objectives',
        name='learning-objectives'),
    url(r'^lesson/(?P<slug>[-\w]*)/materials/$',
        'curricula.views.lesson_detail',
        {'template_name': 'curricula/fragments/materials.html'},
        name='lesson-materials'),
    url(r'^lesson/(?P<slug>[-\w]*)/preparation/$',
        'curricula.views.lesson_detail',
        {'template_name': 'curricula/fragments/preparation.html'},
        name='lesson-preparation'),
    url(r'background-information/(?P<id>\d+)/$',
        'curricula.views.background_information',
        name='background-information'),
    url(r'get_breakout_terms/(?P<id>\d+)/$',
        'curricula.views.get_breakout_terms',
        name='get-breakout-terms'),
    url(r'^activity/$',
        'django.views.generic.list_detail.object_list',
        {'template_name': 'curricula/activity_list.html',
         'queryset': Activity.objects.filter(published=True), },
        name="activity-list",
    ),
    url(r'^activity/(?P<slug>[-\w]*)/$',
        'curricula.views.activity_detail',
        {'template_name': 'curricula/activity_detail.html'},
        name='activity-detail'
    ),
    url(r'^lesson/$',
        'django.views.generic.list_detail.object_list',
        {'template_name': 'curricula/lesson_list.html',
         'queryset': Lesson.objects.filter(published=True), },
        name="lesson-list",
    ),
    url(r'^lesson/(?P<slug>[-\w]*)/$',
        'curricula.views.lesson_detail',
        {'template_name': 'curricula/lesson_detail.html'},
        name='lesson-detail'
    ),
    url(r'activity_info/(?P<ids>.+)$',
        'activity_info',
        name='activity-info'),

    url(r'^standards/$',
        'curricula.views.standard_type_list',
        name='standard-type-list'
    ),

    url(r'^standards/(?P<standard_type>[-\w]*)/$',
        'curricula.views.standard_type_detail',
        name='standard-type-detail'
    ),

)
