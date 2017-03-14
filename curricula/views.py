from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.template.response import TemplateResponse
import json

from curricula.models import Activity, CategoryIdea, Lesson, Standard, IdeaCategory, Unit
from curricula.utils import activities_info, tags_for_activities

from concepts.models import Concept, ConceptItem

from curricula.settings import RELATION_MODELS, KEY_IMAGE, RC_SLIDE


def activity_detail(request, slug, preview=False, template_name='curricula/activity_detail.html'):
    if preview:
        activity = get_object_or_404(Activity, slug=slug)
    else:
        activity = get_object_or_404(Activity, slug=slug, published=True)

    resourceitems = activity.resource_items.all()
    # Sort alphabetically
    resourceitems = resourceitems.order_by('resource_type')

    pops = [x.content_object for x in activity.get_relation_type('Pictures of Practice') if x.content_object]
    msws = [x.content_object for x in activity.get_relation_type('Model Student Work') if x.content_object]
    return TemplateResponse(request, template_name, {
        'activity': activity,
        'object': activity,
        'resourceitems': resourceitems,
        'credit_details': activity.get_credit_details(),
        'model_student_work': msws,
        'pictures_of_practice': pops,
        'preview': preview,
    })


def activity_list(request, preview=False, template_name='curricula/activity_list.html'):
    if preview:
        activities = Activity.objects.all()
    else:
        activities = Activity.objects.filter(published=True)

    return TemplateResponse(request, template_name, {
        'activity_list': activities,
        'object_list': activities,
    })


def idea_category(request, slug, preview=False, template_name='curricula/idea_category.html'):
    if preview:
        category = get_object_or_404(IdeaCategory, slug=slug)
    else:
        category = get_object_or_404(IdeaCategory, slug=slug, published=True)

    credit_details = {}
    if category.credit:
        for detail in category.credit.credit_details.all():
            if detail.credit_category not in credit_details:
                credit_details[detail.credit_category] = []
            credit_details[detail.credit_category].append(detail.entity)

    ideas = []
    for categoryidea in CategoryIdea.objects.filter(category=category):
        ideas.append(categoryidea.idea)

    return TemplateResponse(request, template_name, {
        'category': category,
        'object': category,
        'ideas': ideas,
        'credit_details': credit_details,
        'preview': preview,
    })


def activity_info(request, ids):
    """
    Return a json serialized datastream of activity infomation based on the
    requested id combination.
    """
    result = json.dumps(activities_info(ids))
    return HttpResponse(result, mimetype="text/javascript")


def background_information(request, id):
    lesson = get_object_or_404(Lesson, id=id)

    context = {'background_information': lesson.get_background_information(), }
    return TemplateResponse(request, 'curricula/fragments/bg_info.html', context)


def learning_objectives(request, id):
    lesson = get_object_or_404(Lesson, id=id)

    context = {'learning_objectives': lesson.get_learning_objectives(), }
    return TemplateResponse(request, 'curricula/fragments/objectives.html', context)


def get_breakout_terms(request, id):
    '''
    AJAX response for TinyMCE for Glossification.
    '''
    activity = get_object_or_404(Activity, id=id)
    breakout_terms = activity.vocabulary.all()
    terms = [gt.word_lower for gt in breakout_terms]
    res = json.dumps(terms)
    return HttpResponse(res)


def standard_type_list(request):
    """
    Listing of standard types
    """
    from .settings import STD_TYPE_SLUG_MAP
    context = {'standard_types': STD_TYPE_SLUG_MAP}
    return TemplateResponse(request, 'curricula/standard_type_list.html', context)


def standard_type_detail(request, standard_type):
    """
    Detail of a standard types
    """
    try:
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
        return TemplateResponse(request, template, context)
    except KeyError:
        raise Http404


def credit_details(obj):
    credit_details = {}
    if obj.credit:
        for detail in obj.credit.credit_details.all():
            if detail.credit_category not in credit_details:
                credit_details[detail.credit_category] = []
            credit_details[detail.credit_category].append(detail.entity)

    return credit_details


def get_lesson_tags(lesson, activity_ids):
    ctype = ContentType.objects.get_for_model(Lesson)
    params = dict(content_type=ctype, object_id=lesson.id, weight__gt=0)
    con_ids = ConceptItem.objects.filter(**params).values_list('tag', flat=True)
    if con_ids:
        return Concept.objects.filter(id__in=con_ids)
    else:
        return tags_for_activities(activity_ids)


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
            activities = lesson.activities.all()
        else:
            activities = lesson.activities.get_published()

    context = {
        'lesson': lesson,
        'object': lesson,
        'activities': activities,
        'credit_details': credit_details(lesson),
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

    activity_info['tags'] = get_lesson_tags(lesson, activity_ids)

    context.update(activity_info)
    return TemplateResponse(request, template_name, context)


def lesson_info(request, ids, l_id):
    result = json.dumps(activities_info(ids, l_id))
    return HttpResponse(result, content_type="text/javascript")


def unit_detail(request, slug, preview=False, template_name='curricula/unit_detail.html'):
    if preview:
        unit = get_object_or_404(Unit, slug=slug)
    else:
        unit = get_object_or_404(Unit, slug=slug, published=True)

    ctype = ContentType.objects.get_for_model(Unit)
    concepts = ConceptItem.objects.filter(content_type=ctype, object_id=unit.id, weight__gt=0)
    glossary = unit.get_vocabulary()
    glossary.sort(key=lambda x: x.word_lower)

    return TemplateResponse(request, template_name, {
        'unit': unit,
        'object': unit,
        'preview': preview,
        'glossary': glossary,
        'key_concepts': concepts,
        'credit_details': credit_details(unit),
    })
