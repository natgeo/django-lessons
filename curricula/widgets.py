from django.conf import settings
from django.contrib.admin import widgets
from django.utils.safestring import mark_safe

try:
    from education.edu_core.models import GlossaryTerm
except ImportError:
    from .models import GlossaryTerm

class VocabularyIdWidget(widgets.ForeignKeyRawIdWidget):
    def __init__(self, rel, attrs=None):
        self.widget = widgets.ForeignKeyRawIdWidget
        super(VocabularyIdWidget, self).__init__(rel, attrs)

    def render(self, name, value, attrs=None):
        output = [super(VocabularyIdWidget, self).render(name, value, attrs)]

        if value:
            try:
                encyclopedic = GlossaryTerm.objects.get(id=value).encyclopedic
                if encyclopedic:
                    src = settings.STATIC_URL + 'sites/education/i/ico_ee.png'

                    output.append(u'<a href="/admin/edu_core/encyclopedicentry/%s/" target="_blank">' % encyclopedic.id)
                    output.append(u'<img src="%s" alt="Encyclopedic Entry available"/></a>' % src)
            except GlossaryTerm.DoesNotExist:
                pass
        return mark_safe(u''.join(output))
