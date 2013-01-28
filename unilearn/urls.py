from django.conf.urls import patterns, include, url
from django.contrib import admin

from unilearn.views import IndexPageView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('lecture.urls')),

    url(r'^$', IndexPageView.as_view(), name='index'),

    url(r'^admin/', include(admin.site.urls)),
)
