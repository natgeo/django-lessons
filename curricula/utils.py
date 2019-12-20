from collections import defaultdict
from django.template.loader import render_to_string

from bs4 import BeautifulSoup

from curricula.settings import INTERNET_ACCESS_TYPES
from edumetadata.models import Subject


def unique(self, *args):
    """
    Get the unique items of args
    """
    if args:
        return list(set(*args))
    else:
        return []


def ul_as_list(html):
    if html:
        soup = BeautifulSoup(html)
        items = [str(li).replace("<li>", "").replace("</li>", "") for li in soup('li')]
        return [x for x in items if x != "None"]
    return []


def list_as_ul(items):
    if items:
        return "<ul>%s</ul>" % "".join("<li>%s</li>" % x for x in items)
    else:
        return ""


def truncate(string, limit=48, fill="..."):
    """
    Truncate string to limit. If greater than limit,
    truncate to the length fill and add fill string
    """
    if len(string) <= limit:
        return string
    trunc_limit = limit - len(fill)
    return "%s%s" % (string[:trunc_limit], fill)


def tags_for_activities(ids):
    """
    De-duplicate tags on a comma-delimited list of activity ids
    """
    from concepts.models import Concept, ConceptItem
    from curricula.models import Activity
    from django.contrib.contenttypes.models import ContentType

    ctype = ContentType.objects.get_for_model(Activity)
    act_ids = [int(x) for x in ids.split(',')]

    params = dict(content_type=ctype, object_id__in=act_ids, weight__gt=0)
    con_ids = ConceptItem.objects.filter(**params).values_list('tag', flat=True)
    return Concept.objects.filter(id__in=con_ids)


def tags_for_object(obj):
    from concepts.models import ConceptItem
    from django.contrib.contenttypes.models import ContentType

    ctype = ContentType.objects.get_for_model(obj)
    tagitems = ConceptItem.objects.filter(
        content_type=ctype,
        object_id=obj.pk).exclude(tag__name='')
    return [x.tag for x in tagitems]


def keyword_wrapper(obj, model, ar_a=1, tags=None):
    from concepts.models import ConceptItem
    from django.contrib.contenttypes.models import ContentType

    tags = tags or tags_for_object(obj)
    ctype = ContentType.objects.get_for_model(model)
    concept_items = ConceptItem.objects.filter(content_type=ctype, tag__in=tags)
    ids = [ci.object_id for ci in concept_items.exclude(object_id=obj.id)]

    return model.objects.filter(id__in=set(ids))


def get_gfk_items(ctypes_and_ids):
    """
    given a list of content type and id tuples, get all the objects and return
    them as a list
    """
    from django.contrib.contenttypes.models import ContentType
    gfks = defaultdict(list)
    objects = []
    for ctype, obj_id in ctypes_and_ids:
        gfks[ctype].append(obj_id)

    for ctype, obj_ids in list(gfks.items()):
        objs = ContentType.objects.get_for_id(ctype).model_class()._default_manager.in_bulk(obj_ids)
        objects.extend(list(objs.values()))
    return objects


def group_resources(resources):
    """
    group a list of resources by their resource_type
    """
    from contentrelations.base import ResourceIterator
    items = resources
    output = defaultdict(list)
    if not isinstance(resources, ResourceIterator):
        items = ResourceIterator(resources)
    for obj in items:
        output[obj.resource_type].append({
            'pk': obj.id,
            'url': obj.url,
            'title': obj.title,
            'type': obj.resource_type,
        })
    return output


def activities_info(ids, l_id=None):
    """
    De-duplicate and aggregate fields on a comma-delimited list of activity ids
    """
    from resource_carousel.models import ExternalResource as ResourceModel
    from reference.models import GlossaryTerm
    from curricula.models import (Activity, TeachingApproach, TeachingMethodType,
                                  Standard, Material, Skill, PluginType,
                                  TechSetupType, PhysicalSpaceType, GroupingType,
                                  Lesson, ObjectiveRelation)

    from concepts.models import Concept, ConceptItem
    from django.contrib.contenttypes.models import ContentType
    from django.db.models import Avg

    if l_id:
        ctype = ContentType.objects.get_for_model(Lesson)
        objectives_list = ObjectiveRelation.objects.filter(content_type=ctype,
                                                           object_id=l_id)
        learning_objs = set([objrel.objective for objrel in objectives_list])
        resources = set(Lesson.objects.get(id=l_id).resources.all().values_list('object_type_id', 'object_id'))
        items = ConceptItem.objects.filter(content_type=ctype, object_id=l_id, weight__gt=0)
    else:
        learning_objs = set()
        resources = set()
        items = []

    ctype = ContentType.objects.get_for_model(Activity)

    act_ids = [int(x) for x in ids.split(',')]
    activities = Activity.objects.filter(id__in=act_ids)
    subjects = set()
    teach_approach = set()
    teach_meth = set()
    skills = set()
    standards = set()
    materials = set()

    # can't aggregate this, really need to take most specific.
    # If one activity is optional and one is required, inet_activity
    # must be required.
    inet_access = 1
    plugins = set()
    tech = set()
    phys_space = set()
    setup = []  # text fields. Can't really dedup them with sets.
    grouping = set()
    access_notes = []  # text fields. Can't really dedup them with sets.
    other = []  # text fields. Can't really dedup them with sets.
    glossary = set()
    further_expl = set()

    # we can't get the related fields using values querysets in this version
    # of Django. Instead, we'll query them separately and replace the id
    # with the tag information we need
    if len(items) <= 0:
        items = ConceptItem.objects.filter(content_type=ctype, object_id__in=act_ids, weight__gt=0)
    concepts = list(items.values('tag').annotate(avg_weight=Avg('weight')).order_by('tag').distinct())
    con_ids = [x['tag'] for x in concepts]
    tags = Concept.objects.filter(id__in=con_ids).values('id', 'name', 'url')
    tag_dict = dict((x['id'], x) for x in tags)
    for tag in concepts:
        tag['tag'] = tag_dict[tag['tag']]
        tag['weight'] = int(round(tag['avg_weight'] / 5.0) * 5)
    for activity in activities:
        subjects |= set(activity.subjects.values_list('id', flat=True))
        teach_approach |= set(activity.teaching_approaches.values_list('id', flat=True))
        teach_meth |= set(activity.teaching_method_types.values_list('id', flat=True))
        skills |= set(activity.skills.values_list('id', flat=True))
        standards |= set(activity.standards.values_list('id', flat=True))
        materials |= set(activity.materials.values_list('id', flat=True))

        objectives_list = ObjectiveRelation.objects.filter(
            content_type=ctype, object_id=activity.id)
        learning_objs |= set([objrel.objective for objrel in objectives_list])
        resources |= set(activity.resources.all().values_list('object_type_id', 'object_id'))

        if activity.internet_access_type > inet_access:
            inet_access = activity.internet_access_type
        plugins |= set(activity.plugin_types.values_list('id', flat=True))
        tech |= set(activity.tech_setup_types.values_list('id', flat=True))
        phys_space |= set(activity.physical_space_types.values_list('id', flat=True))
        setup.append(activity.setup)
        grouping |= set(activity.grouping_types.values_list('id', flat=True))
        access_notes.append(activity.accessibility_notes)
        other.append(activity.other_notes)
        glossary |= set(activity.vocabulary.values_list('id', flat=True))
        further_expl |= set(activity.resource_items.values_list('id', flat=True))

    output = {}

    li_template = "<li>%s</li>"

    output['learning_objectives'] = "".join([li_template % x.text for x in learning_objs])
    if output['learning_objectives'] == "":
        output['learning_objectives'] = li_template % "None"
    output['teaching_approaches'] = "".join([li_template % x for x in TeachingApproach.objects.filter(id__in=list(teach_approach)).values_list('name', flat=True)])
    if output['teaching_approaches'] == "":
        output['teaching_approaches'] = li_template % "None"
    output['teaching_methods'] = "".join([li_template % x for x in TeachingMethodType.objects.filter(id__in=list(teach_meth)).values_list('name', flat=True)])
    if output['teaching_methods'] == "":
        output['teaching_methods'] = li_template % "None"
    output['materials'] = "".join([li_template % x for x in Material.objects.filter(id__in=list(materials)).values_list('name', flat=True)])
    if output['materials'] == "":
        output['materials'] = li_template % "None"
    output['required_tech'] = ""
    if inet_access:
        output['required_tech'] += "<li>Internet access: %s</li>" % dict(INTERNET_ACCESS_TYPES)[inet_access]
    tst = TechSetupType.objects.filter(id__in=list(tech)).values_list('title', flat=True)
    if tst:
        output['required_tech'] += "<li>Tech Setup: %s</li>" % ", ".join(tst)
    pis = PluginType.objects.filter(id__in=list(plugins)).values_list("name", flat=True)
    if pis:
        output['required_tech'] += "<li>Plug-Ins: %s</li>" % ", ".join(pis)
    output['physical_space'] = "".join([li_template % x for x in PhysicalSpaceType.objects.filter(id__in=list(phys_space)).values_list('name', flat=True)])
    if output['physical_space'] == "":
        output['physical_space'] = li_template % "None"
    output['setup'] = "".join(setup)
    if output['setup'] == "":
        output['setup'] = "<ul><li>None</li></ul>"
    output['grouping'] = "".join([li_template % x for x in GroupingType.objects.filter(id__in=list(grouping)).values_list('name', flat=True)])
    if output['grouping'] == "":
        output['grouping'] = li_template % "None"
    output['accessibility_notes'] = "".join(access_notes)
    if output['accessibility_notes'] == "":
        output['accessibility_notes'] = "<ul><li>None</li></ul>"
    output['other_notes'] = "".join(other)
    # if output['other_notes'] == "":
    #     output['other_notes'] = "<ul><li>None</li></ul>"

    # these are complex and require rendering
    ctxt = {'objects': Subject.objects.filter(id__in=list(subjects))}
    output['subjects'] = render_to_string('widgets/tree_list.html', ctxt)

    ctxt = {'objects': Skill.objects.filter(id__in=list(skills))}
    output['skills'] = render_to_string('widgets/tree_list.html', ctxt)

    ctxt = {'objects': Standard.objects.filter(id__in=list(standards))}
    output['standards'] = render_to_string('widgets/standards.html', ctxt)

    objects = GlossaryTerm.objects.select_related().filter(id__in=list(glossary))
    ctxt = {'vocabulary': objects}
    output['glossary'] = render_to_string('widgets/vocabulary_table.html', ctxt)
    output['vocabulary'] = []  # ctxt['objects']
    for obj in objects:
        if obj.generic_article:
            generic_article_slug = {'slug': obj.generic_article.slug}
        else:
            generic_article_slug = None
        output['vocabulary'].append({
            'word': obj.word,
            'phonetic': obj.phonetic,
            'get_part_of_speech_display': obj.get_part_of_speech_display(),
            'definition': obj.definition,
            'generic_article': generic_article_slug})

    ctxt = {'objects': ResourceModel.objects.select_related().filter(id__in=list(further_expl)).order_by('resource_type')}
    output['further_exploration'] = render_to_string('widgets/further_exploration_list.html', ctxt)
    ctxt = {'key_concepts': concepts}
    output['key_concepts'] = render_to_string('widgets/key_concepts_list.html', ctxt)

    # We'll keep resources as is, and call the javascript to render it.
    objects = get_gfk_items(resources)
    output['resources'] = group_resources(objects)
    return output
