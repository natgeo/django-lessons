from collections import defaultdict

from django.template.loader import render_to_string

from BeautifulSoup import BeautifulSoup

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
        return [li.contents[0] for li in soup('li')]
    return []


def list_as_ul(items):
    return "<ul>%s</ul>" % "".join("<li>%s</li>" % x for x in items)


def truncate(string, limit=48, fill="..."):
    """
    Truncate string to limit. If greater than limit,
    truncate to the length fill and add fill string
    """
    if len(string) <= limit:
        return string
    trunc_limit = limit - len(fill)
    return u"%s%s" % (string[:trunc_limit], fill)


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
    from concepts.models import Concept, ConceptItem
    from django.contrib.contenttypes.models import ContentType

    ctype = ContentType.objects.get_for_model(obj)
    tagitems = ConceptItem.objects.filter(
        content_type=ctype,
        object_id=obj.pk).exclude(tag__name='')
    return [x.tag for x in tagitems]


def keyword_wrapper(obj, model, ar_a=1, tags=None):
    from concepts.models import Concept, ConceptItem
    from django.contrib.contenttypes.models import ContentType

    tags = tags or tags_for_object(obj)
    ctype = ContentType.objects.get_for_model(model)
    concept_items = ConceptItem.objects.filter(content_type=ctype, tag__in=tags)
    ids = [ci.object_id for ci in concept_items.exclude(object_id=obj.id)]

    return model.objects.filter(id__in=set(ids))


def activities_info(ids, l_id=None):
    """
    De-duplicate and aggregate fields on a comma-delimited list of activity ids
    """
    from resourcecarousel.models import ExternalResource as ResourceModel
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
    else:
        learning_objs = set()

    ctype = ContentType.objects.get_for_model(Activity)

    act_ids = [int(x) for x in ids.split(',')]
    activities = Activity.objects.filter(id__in=act_ids)
    subjects = set()
    teach_approach = set()
    teach_meth = set()
    skills = set()
    standards = set()
    materials = set()
    resources = defaultdict(list)
    inet_access = 1  # can't aggregate this, really need to take most specific.
                     # If one activity is optional and one is required, inet_activity
                     # must be required.
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
    items = ConceptItem.objects.filter(content_type=ctype, object_id__in=act_ids)
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
        if activity.internet_access_type > inet_access:
            inet_access = activity.internet_access_type
        plugins |= set(activity.plugin_types.values_list('id', flat=True))
        tech |= set(activity.tech_setup_types.values_list('id', flat=True))
        phys_space |= set(activity.physical_space_types.values_list('id', flat=True))
        setup.append(activity.setup)
        grouping |= set(activity.grouping_types.values_list('id', flat=True))
        access_notes.append(activity.accessibility_notes)
        other.append(activity.other_notes)
        glossary |= set(activity.vocabulary_set.values_list('glossary_term__id', flat=True))
        further_expl |= set(activity.resourceitem_set.values_list('resource__id', flat=True))

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
    output['subjects'] = render_to_string('includes/tree_list.html', ctxt)

    ctxt = {'objects': Skill.objects.filter(id__in=list(skills))}
    output['skills'] = render_to_string('includes/tree_list.html', ctxt)

    ctxt = {'objects': Standard.objects.filter(id__in=list(standards))}
    output['standards'] = render_to_string('includes/standards.html', ctxt)

    objects = GlossaryTerm.objects.filter(id__in=list(glossary)).values('word', 'definition', 'part_of_speech')
    ctxt = {'objects': objects}
    output['glossary'] = render_to_string('includes/vocabulary_list.html', ctxt)

    ctxt = {'objects': ResourceModel.objects.select_related().filter(id__in=list(further_expl))}
    output['further_exploration'] = render_to_string('includes/further_exploration_list.html', ctxt)
    ctxt = {'key_concepts': concepts}
    output['key_concepts'] = render_to_string('includes/key_concepts_list.html', ctxt)

    # We'll keep resources as is, and call the javascript to render it.
    output['resources'] = resources
    return output
