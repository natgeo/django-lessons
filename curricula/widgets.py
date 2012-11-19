from django.conf import settings
from django.contrib.admin import widgets
from django.utils.safestring import mark_safe

from education.edu_core.models import GlossaryTerm


class VocabularyIdWidget(widgets.ForeignKeyRawIdWidget):
    def __init__(self, *args, **kwargs):
        self.widget = widgets.ForeignKeyRawIdWidget
        super(VocabularyIdWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        output = [super(VocabularyIdWidget, self).render(name, value, attrs)]

        if value:
            try:
                encyclopedic = GlossaryTerm.objects.get(id=value).generic_article
                if encyclopedic:
                    src = settings.STATIC_URL + 'sites/education/i/ico_ee.png'

                    output.append(u'<a href="/admin/reference/genericarticle/%s/" target="_blank">' % encyclopedic.id)
                    output.append(u'<img src="%s" alt="Encyclopedic Entry available"/></a>' % src)
            except GlossaryTerm.DoesNotExist:
                pass
        return mark_safe(u''.join(output))
