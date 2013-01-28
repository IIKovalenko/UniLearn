from django.conf.urls import patterns, include, url

from lecture.views import CourseListView, CourseDetailView, LectureDetailView, CourseCreateView, LectureCreateView


urlpatterns = patterns('',
    url(r'^course/list/$', CourseListView.as_view(), name='course-list'),
    url(r'^course/add/$', CourseCreateView.as_view(), name='course-add'),
    url(r'^lecture/add/$', LectureCreateView.as_view(), name='lecture-add'),
    url(r'^course/(?P<pk>\d+)/$', CourseDetailView.as_view(), name='course-detail'),
    url(r'^course/(?P<course_pk>\d+)/(?P<lecture_num>\d+)/$', LectureDetailView.as_view(), name='lecture-detail'),
)
