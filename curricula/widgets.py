import json
from django.conf import settings
from django.contrib.admin import widgets
from django.utils.safestring import mark_safe
from django import forms
from django.forms.widgets import Widget
from django.utils.encoding import force_text
from django.template.loader import render_to_string

try:
    from django.contrib.admin.templatetags.admin_static import static
except ImportError:
    def static(somestring):
        return "%s%s" % (settings.ADMIN_MEDIA_PREFIX, somestring)

from reference.models import GlossaryTerm


class VocabularyIdWidget(widgets.ForeignKeyRawIdWidget):
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


class SpecificGenericRawIdWidget(forms.TextInput):
    def __init__(self, rel, attrs=None):
        self.rel = rel
        super(SpecificGenericRawIdWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        # if 'class' not in attrs:
        #     attrs['class'] = 'vGenericRawIdAdminField'  # The JavaScript looks for this hook.
        output = [super(SpecificGenericRawIdWidget, self).render(name, value, attrs)]
        output.append('<a id="lookup_id_%(name)s" class="related-lookup" onclick="return showGenericRequiredModelLookupPopup(this, \'%(rel)s\');" href="#">' %
            {'name': name, 'rel': self.rel})
        output.append('&nbsp;<img src="%s" width="16" height="16" alt="%s" /></a>' % (static('admin/img/selector-search.gif'), 'Lookup'))
        return mark_safe(u''.join(output))

    class Media:
        js = ('js/genericcollections.js', )


class DynalistWidget(Widget):
    class Media:
        css = {
            'all': ('curricula/dynalist.css', ),
        }
        js = ('curricula/dynalist.js', )

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(value)
        return render_to_string('admin/curricula/dynalist.html', {
            'value': value,
            'name': name,
            'attrs': attrs,
            'items': json.loads(value) if value else [],
        })
