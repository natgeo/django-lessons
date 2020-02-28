from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.views.static import serve

import contentrelations

admin.autodiscover()
contentrelations.autodiscover()


urlpatterns = [
    url(r'^curricula/', include('curricula.urls')),
    url(r'^concepts/', include('concepts.urls')),
    # url(r'^publishing/', include('publisher.urls')),
    url(r'^admin/', include(admin.site.urls)),
    ]

urlpatterns += [
    url(r'^tinymce/', include('tinymce.urls')),
    # url(r'^admin/(.*)', admin.site.root),
    url(r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:], serve,
        {"document_root": settings.MEDIA_ROOT}),
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], serve,
        {"document_root": settings.MEDIA_ROOT}),
    ]
