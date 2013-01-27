from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404

from lecture.models import Course, Lecture


class CourseListView(ListView):
    model = Course
    template_name='lecture/course_list.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name='lecture/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['lectures'] = Lecture.objects.filter(course = context['course'])
        return context
    

class LectureDetailView(TemplateView):
    template_name='lecture/lecture_detail.html'

    def get_context_data(self, **kwargs):
        context = super(LectureDetailView, self).get_context_data(**kwargs)
        context['lecture'] = Lecture.objects.get(course__pk = self.kwargs['course_pk'], number = self.kwargs['lecture_num'])
        return context
