from django.conf.urls import url
from django.views.generic.list_detail import object_list

from .models import Activity, Lesson
from .views import (
    activity_detail, activity_info, background_information, get_breakout_terms,
    learning_objectives, lesson_detail, standard_type_detail, standard_type_list
)


urlpatterns = [
    url(r'objectives/(?P<id>\d+)/$', learning_objectives,
        name='learning-objectives'),
    url(r'^lesson/(?P<slug>[-\w]*)/materials/$', lesson_detail,
        {'template_name': 'curricula/fragments/materials.html'},
        name='lesson-materials'),
    url(r'^lesson/(?P<slug>[-\w]*)/preparation/$', lesson_detail,
        {'template_name': 'curricula/fragments/preparation.html'},
        name='lesson-preparation'),
    url(r'background-information/(?P<id>\d+)/$', background_information,
        name='background-information'),
    url(r'get_breakout_terms/(?P<id>\d+)/$', get_breakout_terms,
        name='get-breakout-terms'),
    url(r'^activity/$', object_list,
        {'template_name': 'curricula/activity_list.html',
         'queryset': Activity.objects.filter(published=True), },
        name="activity-list",),
    url(r'^activity/(?P<slug>[-\w]*)/$', activity_detail,
        {'template_name': 'curricula/activity_detail.html'},
        name='activity-detail'),
    url(r'^lesson/$', object_list,
        {'template_name': 'curricula/lesson_list.html',
         'queryset': Lesson.objects.filter(published=True), },
        name="lesson-list",),
    url(r'^lesson/(?P<slug>[-\w]*)/$', lesson_detail,
        {'template_name': 'curricula/lesson_detail.html'},
        name='lesson-detail'),
    url(r'activity_info/(?P<ids>.+)$', activity_info, name='activity-info'),
    url(r'^standards/$', standard_type_list, name='standard-type-list'),
    url(r'^standards/(?P<standard_type>[-\w]*)/$', standard_type_detail,
        name='standard-type-detail'),
]
