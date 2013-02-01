from django.views.generic import ListView, TemplateView, CreateView, FormView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from .models import Course, Lecture
from exam.forms import LectureTestForm
from exam.factories import TestQuestionFactory
from exam.models import LectureTest


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
    

class LectureDetailView(FormView):
    template_name = 'lecture/lecture_detail.html'
    form_class = LectureTestForm

    def get_success_url(self):
        return reverse('index')

    def get_form_kwargs(self):
        kwargs = super(LectureDetailView, self).get_form_kwargs()
        self.lecture = Lecture.objects.get(course__pk = self.kwargs['course_pk'], number = self.kwargs['lecture_num'])
        test_info = LectureTest.get_lecture_test_info(self.lecture.pk)
        kwargs.update({'test_info': test_info})
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(LectureDetailView, self).get_context_data(**kwargs)
        context['lecture'] = self.lecture
        if 'form' in kwargs:
            context['form'] = kwargs['form']
        else:
            context['form'] = LectureTestForm.get_lecture_test_form(self.lecture.pk)
        print context['form'].errors
        return context


class CourseCreateView(CreateView):
    template_name='lecture/course_create.html'
    model = Course


class LectureCreateView(CreateView):
    template_name='lecture/lecture_create.html'
    model = Lecture
