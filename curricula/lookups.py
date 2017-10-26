from education.edu_core.models import GlossaryTerm, Resource

from selectable.base import ModelLookup
from selectable.registry import registry


class GlossaryTermLookup(ModelLookup):
    model = GlossaryTerm
    search_fields = ('word__icontains', )

    def get_item_id(self, item):
        return item.id


class ResourceLookup(ModelLookup):
    model = Resource
    search_fields = ('title__icontains', )

    def get_item_id(self, item):
        return item.id

registry.register(GlossaryTermLookup)
