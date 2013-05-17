from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.utils import simplejson

from settings import RELATION_MODELS, KEY_IMAGE, RC_SLIDE
from curricula.models import Activity, Lesson, Standard, IdeaCategory
from curricula.utils import activities_info, tags_for_activities


def activity_detail(request, slug, preview=False, template_name='curricula/activity_detail.html'):
    if preview:
        activity = get_object_or_404(Activity, slug=slug)
    else:
        activity = get_object_or_404(Activity, slug=slug, published=True)

    audience = None
    getvars = request.GET.copy()
    if 'ar_a' in getvars:
        audience = int(getvars['ar_a'])
    resourceitems = activity.resourceitem_set.all()
    # Sort alphabetically
    resourceitems = resourceitems.order_by('resource__resource_category_type')
    if audience:
        resourceitems = [resourceitem for resourceitem in resourceitems
            if audience in resourceitem.resource.appropriate_for_audience_type_pks]

    return render_to_response(template_name, {
        'activity': activity,
        'resourceitems': resourceitems,
        'credit_details': activity.get_credit_details(),
        'model_student_work': activity.model_student_work(audience),
        'pictures_of_practice': activity.pictures_of_practice(audience),
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
    if 'activities' in getvars:
        activities = getvars['activities']
    else:
        if preview:
            activities = lesson.get_activities()
        else:
            activities = lesson.get_activities({'activity__published': True})

    credit_details = {}
    if lesson.credit:
        for detail in lesson.credit.credit_details.all():
            if detail.credit_category not in credit_details:
                credit_details[detail.credit_category] = []
            credit_details[detail.credit_category].append(detail.entity)

    context = {
        'lesson': lesson,
        'activities': activities,
        'credit_details': credit_details,
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
    activity_info = activities_info(activity_ids, lesson.id)
    activity_info['tags'] = tags_for_activities(activity_ids)
    context.update(activity_info)
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def idea_category(request, slug, preview=False, template_name='curricula/idea_category.html'):
    if preview:
        category = get_object_or_404(IdeaCategory, slug=slug)
    else:
        category = get_object_or_404(IdeaCategory, slug=slug, published=True)

    audience = None
    getvars = request.GET.copy()
    if 'ar_a' in getvars:
        audience = int(getvars['ar_a'])

    credit_details = {}
    if category.credit:
        for detail in category.credit.credit_details.all():
            if detail.credit_category not in credit_details:
                credit_details[detail.credit_category] = []
            credit_details[detail.credit_category].append(detail.entity)

    return render_to_response(template_name, {
        'category': category,
        'ideas': [ci.idea for ci in category.categoryidea_set.all() if audience in ci.idea.appropriate_for.get_set_bits()],
        'credit_details': credit_details,
        'preview': preview,
    }, context_instance=RequestContext(request))


def activity_info(request, ids):
    """
    Return a json serialized datastream of activity infomation based on the
    requested id combination.
    """
    result = simplejson.dumps(activities_info(ids))
    return HttpResponse(result, mimetype="text/javascript")


def background_information(request, id):
    lesson = get_object_or_404(Lesson, id=id)

    context = {'background_information': lesson.get_background_information(), }
    return render_to_response('curricula/fragments/bg_info.html',
                              context,
                              context_instance=RequestContext(request))


def learning_objectives(request, id):
    lesson = get_object_or_404(Lesson, id=id)

    context = {'learning_objectives': lesson.get_learning_objectives(), }
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


def standard_type_list(request):
    """
    Listing of standard types
    """
    from .settings import STD_TYPE_SLUG_MAP
    context = {'standard_types': STD_TYPE_SLUG_MAP}
    return render_to_response('curricula/standard_type_list.html',
                               context,
                               context_instance=RequestContext(request))


def standard_type_detail(request, standard_type):
    """
    Detail of a standard types
    """
    from .settings import STD_TYPE_SLUG_MAP
    context = {
        'objects': Standard.objects.filter(
            standard_type=STD_TYPE_SLUG_MAP[standard_type]['key']
        ),
        'standard_type': STD_TYPE_SLUG_MAP[standard_type]['name']
    }
    template = (
        "curricula/%s_detail.html" % standard_type,
        "curricula/standard_type_detail.html"
    )
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))
