from django import template
from django.contrib.contenttypes.models import ContentType

from curricula.models import Activity, Lesson, ActivityRelation, LessonRelation
from curricula.settings import KEY_IMAGE, RESOURCE_CAROUSEL, RC_SLIDE

register = template.Library()

tabs = (
    ('Overview', 'Directions', 'Objectives', 'Background & Vocabulary', 'Credits, Sponsors, Partners'),
    ('Global Metadata', 'Content Related Metadata', 'Time and Date Metadata'),
    ('Publishing',),
)

@register.filter(name='tab_num')
def tab_num(fieldset):
    for count, fieldsets in enumerate(tabs):
        if fieldset.name in fieldsets:
            return count
    return 0

def get_model(field, setting):
    for name, model in setting:
        if field == name:
            return model
    return None

@register.filter(name='get_activity_model')
def get_activity_model(field):
    return get_model(field, [x for x in (KEY_IMAGE, RESOURCE_CAROUSEL) if x is not None])

@register.filter(name='get_lesson_model')
def get_lesson_model(field):
    return get_model(field, (KEY_IMAGE, RC_SLIDE))

@register.filter(name='lesson_slug')
def lesson_slug(id):
    if id:
        return Lesson.objects.get(id=id).slug
    else:
        return None

@register.filter(name='activity_slug')
def activity_slug(id):
    if id:
        return Activity.objects.get(id=id).slug
    else:
        return None

@register.filter(name='activity_thumbnail')
def activity_thumbnail(id):
    try:
        return Activity.objects.get(id=id).thumbnail_html()
    except Activity.DoesNotExist:
        return None

@register.filter(name='lesson_thumbnail')
def lesson_thumbnail(id):
    try:
        return Lesson.objects.get(id=id).thumbnail_html()
    except Lesson.DoesNotExist:
        return None

@register.filter(name='resource_carousel')
def resource_carousel(id):
    app_label, model = RESOURCE_CAROUSEL[1].split('.')
    ctype = ContentType.objects.get(app_label=app_label, model=model)
    activity = Activity.objects.get(id=id)
    ar = ActivityRelation.objects.get(activity=activity, content_type=ctype)

    return ar.content_object.name

@register.filter(name='rc_slide')
def rc_slide(id):
    try:
        lesson = Lesson.objects.get(id=id)
        app_label, model = RC_SLIDE[1].split('.')
        ctype = ContentType.objects.get(app_label=app_label, model=model)
        lr = LessonRelation.objects.get(lesson=lesson, content_type=ctype)

        return lr.content_object.name
    except LessonRelation.DoesNotExist:
        return None

@register.tag('get_related_content_type')
def do_get_related_content_type(parser, token):
    """
    Gets relations to a story based on the content type
    
    {% get_related_content_type item content_type as var_name %}
    
    {% get_related_content_type object Image as photo %}
    """
    try:
        tag_name, obj, content_type, as_txt, var = token.split_contents()
        content_type = content_type.replace("'", '').replace('"', '')
    except ValueError:
        raise template.TemplateSyntaxError("'get_related_content_type' requires an object, content_type and a variable name.")
    return RelatedNode(obj, var, content_type=content_type)

@register.tag('get_relation_type')
def do_get_relation_type(parser, token):
    """
    Gets the relations to a story based on the relation type
    
    {% get_relation_type item relation_type as var_name %}
    
    {% get_relation_type object leadphoto as leadphoto %}
    """
    try:
        tag_name, obj, relation_type, as_txt, var = token.split_contents()
        relation_type = relation_type.replace("'", '').replace('"', '')
    except ValueError:
        raise template.TemplateSyntaxError("'get_relation_type' requires an object, relation_type and a variable name.")
    return RelatedNode(obj, var, relation_type=relation_type)
    

class RelatedNode(template.Node):
    def __init__(self, object, var_name, content_type=None, relation_type=None):
        self.content_type = content_type
        self.relation_type = relation_type
        self.object = template.Variable(object)
        self.var_name = var_name
        
    def render(self, context):
        try:
            the_obj = self.object.resolve(context)
            if self.content_type:
                context[self.var_name] = the_obj.get_related_content_type(self.content_type)
            elif self.relation_type:
                context[self.var_name] = the_obj.get_relation_type(self.relation_type)
            else:
                context[self.var_name] = []
            return ''
        except template.VariableDoesNotExist:
            return ''
