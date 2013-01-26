from django.conf.urls import patterns, include, url

from lecture.views import CoursesListView


urlpatterns = patterns('',
    url(r'^course/list/$', CoursesListView.as_view(), name='course-list'),

)
