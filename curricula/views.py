from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.utils import simplejson
from django.utils.translation import ugettext, ugettext_lazy as _

from settings import RELATION_MODELS, KEY_IMAGE, RC_SLIDE
from curricula.models import Activity, Lesson

def activity_detail(request, slug, preview=False, template_name='curricula/activity_detail.html'):
    if preview:
        activity = get_object_or_404(Activity, slug=slug)
    else:
        activity = get_object_or_404(Activity, slug=slug, published=True)

    return render_to_response(template_name, {
        'activity': activity,
    }, context_instance=RequestContext(request))

def activity_list(request, preview=False, template_name='curricula/activity_list.html'):
    if preview:
        activities = Activity.objects.all()
    else:
        activities = Activity.objects.filter(published=True)
    
    return render_to_response(template_name, {
        'activity_list': activities
    }, context_instance=RequestContext(request))

def lesson_detail(request, slug, preview=False, template_name='curricula/lesson_detail.html'):
    if preview:
        lesson = get_object_or_404(Lesson, slug=slug)
    else:
        lesson = get_object_or_404(Lesson, slug=slug, published=True)

    getvars = request.GET.copy()
    if getvars.has_key('activities'):
        activities = getvars['activities']
    else:
        activities = lesson.get_activities()

    context = {
        'lesson': lesson,
        'activities': activities,
    }

    for field in (KEY_IMAGE, RC_SLIDE):
        related_ctypes = lesson.get_related_content_type(field[0])
        if len(related_ctypes) > 0:
            context[field[0]] = related_ctypes[0].content_object

    for model in RELATION_MODELS:
        name = model.split('.')[1]
        related_ctypes = lesson.get_related_content_type(name)
        if len(related_ctypes) > 0:
            context[name] = related_ctypes[0].content_object

    return render_to_response(template_name, context, context_instance=RequestContext(request))

def background_information(request, id):
    lesson = get_object_or_404(Lesson, id=id)

    context = { 'background_information': lesson.get_background_information(), }
    return render_to_response('curricula/fragments/bg_info.html',
                              context,
                              context_instance=RequestContext(request))

def learning_objectives(request, id):
    lesson = get_object_or_404(Lesson, id=id)

    context = { 'learning_objectives': lesson.get_learning_objectives(), }
    return render_to_response('curricula/fragments/objectives.html',
                              context,
                              context_instance=RequestContext(request))

def get_breakout_terms(request, id):
    '''
    AJAX response for TinyMCE for Glossification.
    '''
    activity = get_object_or_404(Activity, id=id)
    breakout_terms = activity.vocabulary_set.all()
    # user lower case terms
    terms = [gt.glossary_term.word.lower() for gt in breakout_terms]
    res = simplejson.dumps(terms)
    return HttpResponse(res)
