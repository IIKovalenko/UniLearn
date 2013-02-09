from django.conf.urls import patterns, include, url

from .views import ProfileDetailView


urlpatterns = patterns('',
    url(r'^/$', ProfileDetailView.as_view(), name='profile-detail'),
)
