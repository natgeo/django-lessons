from collections import defaultdict

from django.conf import settings
from django.template.loader import render_to_string

from BeautifulSoup import BeautifulSoup

from curricula.settings import INTERNET_ACCESS_TYPES
from edumetadata.models import Subject

from education.edu_core.external_models import EduBundle
from education.edu_core.carousel_renderers import gather_carousel_items
from education.edu_core.models import EncyclopedicEntry

def truncate(string, limit=44):
    return string[:limit] + (string[limit:] and '...')

def ul_as_list(html):
    soup = BeautifulSoup(html)
    return [li.contents[0] for li in soup('li')]

def get_audience_index(key):
    for i in range(1, 6):
        if settings.AUDIENCE_SETTINGS['AUDIENCE_TYPES'][i]['name'] == key:
            return i
    return 0

def get_audience_indices(items):
    return [get_audience_index(item[0]) for item in items if item[1]]


def activities_info(ids):
    """
    De-duplicate and aggregate fields on a comma-delimited list of activity ids
    """
    from curricula.models import (Activity, TeachingApproach, TeachingMethodType, 
                                  Standard, Material, Skill, PluginType, 
                                  TechSetupType, PhysicalSpaceType, GroupingType, 
                                  GlossaryTerm, ResourceItem)
    
    from concepts.models import Concept, ConceptItem
    from django.contrib.contenttypes.models import ContentType
    from django.db.models import Avg
    
    ctype = ContentType.objects.get_for_model(Activity)
    
    act_ids = [int(x) for x in ids.split(',')]
    activities = Activity.objects.filter(id__in=act_ids) #, published=True)
    subjects = set()
    teach_approach = set()
    teach_meth = set()
    skills = set()
    standards = set()
    materials = set()
    resources = defaultdict(list)
    inet_access = 1 # can't aggregate this, really need to take most specific.
                     # If one activity is optional and one is required, inet_activity
                     # must be required.
    plugins = set()
    tech = set()
    phys_space = set()
    setup = [] # text fields. Can't really dedup them with sets.
    grouping = set()
    access_notes = [] # text fields. Can't really dedup them with sets.
    other = [] # text fields. Can't really dedup them with sets.
    prior_knowledge = set()
    prior_act = set()
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
        tag['weight'] = int(round(tag['avg_weight']/5.0)*5)
    for activity in activities:
        subjects |= set(activity.subjects.values_list('id', flat=True))
        teach_approach |= set(activity.teaching_approaches.values_list('id', flat=True))
        teach_meth |= set(activity.teaching_method_types.values_list('id', flat=True))
        skills |= set(activity.skills.values_list('id', flat=True))
        standards |= set(activity.standards.values_list('id', flat=True))
        materials |= set(activity.materials.values_list('id', flat=True))
        
        # These lines add a significant number of queries overall due to the
        # way that the edu_core code implements audience.
        bundle_id = activity.get_relation_type('resource_carousel')[0].content_object.id
        resource_dict = gather_carousel_items(EduBundle.objects.get(id=bundle_id))
        for key, val in resource_dict.items():
            resources[key].extend(val)
        
        if activity.internet_access_type > inet_access:
            inet_access = activity.internet_access_type
        plugins |= set(activity.plugin_types.values_list('id', flat=True))
        tech |= set(activity.tech_setup_types.values_list('id', flat=True))
        phys_space |= set(activity.physical_space_types.values_list('id', flat=True))
        setup.append(activity.setup)
        grouping |= set(activity.grouping_types.values_list('id', flat=True))
        access_notes.append(activity.accessibility_notes)
        other.append(activity.other_notes)
        prior_knowledge.add(activity.prior_knowledge)
        prior_act |= set(activity.prior_activities.values_list('id', flat=True))
        glossary |= set(activity.vocabulary_set.values_list('glossary_term__id', flat=True))
        further_expl |= set(activity.resourceitem_set.values_list('resource__id', flat=True))
    
    output = {}
    
    li_template = "<li>%s</li>"
    
    output['teaching_approaches'] = "".join([li_template % x for x in TeachingApproach.objects.filter(id__in=list(teach_approach)).values_list('name', flat=True)])
    output['teaching_methods'] = "".join([li_template % x for x in TeachingMethodType.objects.filter(id__in=list(teach_meth)).values_list('name', flat=True)])
    output['materials'] = "".join([li_template % x for x in Material.objects.filter(id__in=list(materials)).values_list('name', flat=True)])
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
    output['setup'] = "".join(setup)
    output['grouping'] = "".join([li_template % x for x in GroupingType.objects.filter(id__in=list(grouping)).values_list('name', flat=True)])
    output['accessibility_notes'] = "".join(access_notes)
    output['other_notes'] = "".join(other)
    prior_knowledge.discard(u'<ul>\r\n<li>None</li>\r\n</ul>')
    output['prior_knowledge'] = "".join(prior_knowledge)
    
    # these are complex and require rendering
    ctxt = {'objects': Subject.objects.filter(id__in=list(subjects))}
    output['subjects'] = render_to_string('includes/tree_list.html', ctxt)
    
    ctxt = {'objects': Skill.objects.filter(id__in=list(skills))}
    output['skills'] = render_to_string('includes/tree_list.html', ctxt)
    
    ctxt = {'activities': Activity.objects.filter(id__in=list(prior_act)).values("slug", "title")}
    output['prior_activities'] = render_to_string("includes/prior_activities.html", ctxt)
    
    ctxt = {'objects': Standard.objects.filter(id__in=list(standards))}
    output['standards'] = render_to_string('includes/standards.html', ctxt)
    
    objects = GlossaryTerm.objects.filter(id__in=list(glossary)).values('word', 'definition', 'part_of_speech', 'encyclopedic')
    ee_ids = [x['encyclopedic'] for x in objects]
    ees = dict([(x['id'], x) for x in EncyclopedicEntry.objects.filter(id__in=ee_ids).values('id', 'word', 'slug')])
    ctxt = {'objects': []}
    for item in objects:
        if item['encyclopedic']:
            item['encyclopedic'] = ees[item['encyclopedic']]
        ctxt['objects'].append(item)
    output['glossary'] = render_to_string('includes/vocabulary_list.html', ctxt)
    
    ctxt = {'objects': ResourceItem.objects.select_related().filter(id__in=list(further_expl))}
    output['further_exploration'] = render_to_string('includes/further_exploration_list.html', ctxt)
    ctxt = {'key_concepts': concepts}
    output['key_concepts'] = render_to_string('includes/key_concepts_list.html', ctxt)
    
    # We'll keep resources as is, and call the javascript to render it.
    output['resources'] = resources
    return output
