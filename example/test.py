from curricula.models import Activity

def activity_info(ids):
    """
    De-duplicate and aggregate fields on a comma-delimited list of activity ids
    """
    act_ids = [int(x) for x in ids.split(',')]
    activities = Activity.objects.select_related().filter(id__in=act_ids, published=True)
    subjects = set()
    teach_approach = set()
    teach_meth = set()
    skills = set()
    standards = set()
    materials = set()
    resources = set()
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
    prior_knowledge = [] # text fields. Can't really dedup them with sets.
    prior_act = set()
    glossary = set()
    resources = set()
    for activity in activities:
        subjects |= set(activity.subjects.values_list('id', flat=True))
        teach_approach |= set(activity.teaching_approaches.values_list('id', flat=True))
        teach_meth |= set(activity.teaching_method_types.values_list('id', flat=True))
        skills |= set(activity.skills.values_list('id', flat=True))
        standards |= set(activity.standards.values_list('id', flat=True))
        materials |= set(activity.materials.values_list('id', flat=True))
        
        # look at how /edu/get_resource_carousel_json/{{ resource_carousel.0.object_id }}.json
        # aggregates the resources
        resources |= set(activity.foo.values_list('id', flat=True))
        
        if activity.internet_access_type > inet_access:
            inet_access = activity.internet_access_type
        plugins |= set(activity.plugin_types.values_list('id', flat=True))
        tech |= set(activity.tech_setup_types.values_list('id', flat=True))
        phys_space |= set(activity.physical_space_types.values_list('id', flat=True))
        setup.append(activity.setup)
        grouping |= set(activity.grouping_types.values_list('id', flat=True))
        access_notes.append(activity.accessibility_notes)
        other.append(activity.other_notes)
        prior_knowledge.append(activity.prior_knowledge)
        prior_act |= set(activity.prior_activities.values_list('id', flat=True))
        glossary |= set(activity.vocabulary_set.values_list('id', flat=True))
        resources |= set(activity.resourceitem_set.values_list('id', flat=True))


activity_info('314,315,316')