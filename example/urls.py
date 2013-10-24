from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

import contentrelations
contentrelations.autodiscover()

urlpatterns = patterns('',
    (r'^curricula/', include('curricula.urls')),
    (r'^concepts/', include('concepts.urls')),
  # (r'^publishing/', include('publisher.urls')),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^tinymce/', include('tinymce.urls')),
    # url(r'^admin/(.*)', admin.site.root),
    url(r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:],
        'django.views.static.serve', {"document_root": settings.MEDIA_ROOT}),
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
        'django.views.static.serve', {"document_root": settings.MEDIA_ROOT}),
)
