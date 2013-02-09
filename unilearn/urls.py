from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from unilearn.views import IndexPageView
from account.views import LoginView, LogoutView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('lecture.urls')),
    url(r'^profile', include('account.urls')),
                       
    url(r'^$', IndexPageView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
