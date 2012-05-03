from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.utils import simplejson
from django.utils.translation import ugettext, ugettext_lazy as _

from settings import RELATION_MODELS, KEY_IMAGE, RC_SLIDE
from curricula.models import Activity, Lesson
from curricula.utils import activities_info, tags_for_activities

def activity_detail(request, slug, preview=False, template_name='curricula/activity_detail.html'):
    if preview:
        activity = get_object_or_404(Activity, slug=slug)
    else:
        activity = get_object_or_404(Activity, slug=slug, published=True)

    audience = None
    getvars = request.GET.copy()
    if getvars.has_key('ar_a'):
        audience = int(getvars['ar_a'])
    resourceitems = activity.resourceitem_set.all()
    if audience:
        resourceitems = [resourceitem for resourceitem in resourceitems
            if audience in resourceitem.resource.appropriate_for_audience_type_pks]

    credit_details = {}
    for detail in activity.credit.credit_details.all():
        if detail.credit_category not in credit_details:
            credit_details[detail.credit_category] = []
        credit_details[detail.credit_category].append(detail.entity)

    return render_to_response(template_name, {
        'activity': activity,
        'resourceitems': resourceitems,
        'credit_details': credit_details,
        'preview': preview,
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
        if preview:
            activities = lesson.get_activities()
        else:
            activities = lesson.get_activities({'published': True})

    context = {
        'lesson': lesson,
        'activities': activities,
        'preview': preview,
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
    
    activity_ids = ",".join([str(x.id) for x in activities])
    activity_info = activities_info(activity_ids)
    activity_info['tags'] = tags_for_activities(activity_ids)
    context.update(activity_info)
    return render_to_response(template_name, context, context_instance=RequestContext(request))

def activity_info(request, ids):
    """
    Return a json serialized datastream of activity infomation based on the 
    requested id combination.
    """
    from curricula.utils import activities_info
    result = simplejson.dumps(activities_info(ids))
    return HttpResponse(result, mimetype="text/javascript")

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
