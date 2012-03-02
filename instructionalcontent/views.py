from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _

from settings import RELATION_MODELS, REQUIRED_FIELDS
from instructionalcontent.models import Activity, Lesson

def activity_detail(request, slug, template_name='lessons/activity_detail.html'):
    activity = get_object_or_404(Activity, slug=slug)

    return render_to_response(template_name, {
        'activity': activity,
    }, context_instance=RequestContext(request))

def lesson_detail(request, slug, template_name='lessons/lesson_detail.html'):
    lesson = get_object_or_404(Lesson, slug=slug)

    getvars = request.GET.copy()
    if getvars.has_key('activities'):
        activities = getvars['activities']
    else:
        activities = lesson.get_activities()

    context = {
        'lesson': lesson,
        'activities': activities,
    }

    for field in REQUIRED_FIELDS:
        related_ctypes = lesson.get_related_content_type(field[0])
        if len(related_ctypes) > 0:
            context[field[0]] = related_ctypes[0].content_object

    for model in RELATION_MODELS:
        name = model.split('.')[1]
        related_ctypes = lesson.get_related_content_type(name)
        if len(related_ctypes) > 0:
            context[name] = related_ctypes[0].content_object

    return render_to_response(template_name, context, context_instance=RequestContext(request))