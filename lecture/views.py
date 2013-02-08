from django.views.generic import ListView, TemplateView, CreateView, FormView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from .models import Course, Lecture
from .forms import LectureRegistratinForm
from exam.forms import LectureTestForm
from exam.factories import TestQuestionFactory
from exam.models import LectureTest
from account.models import UserTestStatistics


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
        lectures = Lecture.objects.filter(course = context['course'])
        for i, l in enumerate(lectures):
            lectures[i].status = self.request.user.get_lecture_status(l.pk).status
        context['lectures'] = lectures
        return context
    

class LectureDetailView(FormView):
    template_name = 'lecture/lecture_detail.html'
    form_class = LectureTestForm

    @classmethod
    def update_lecture_status(cls, lecture, user):
        user.read_lecture(lecture.pk)

    def dispatch(self, request, *args, **kwargs):
        self.lecture = Lecture.objects.get(course__pk = self.kwargs['course_pk'], number = self.kwargs['lecture_num'])
        return super(LectureDetailView, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.update_lecture_status(self.lecture, request.user)
        return super(LectureDetailView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('index')

    def get_form_kwargs(self):
        kwargs = super(LectureDetailView, self).get_form_kwargs()
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

    def form_valid(self, form):
        self.request.user.passed_test(self.lecture.pk)
        return super(LectureDetailView, self).form_valid(form)

    def form_invalid(self, form):
        self.request.user.failed_test(self.lecture.pk)
        return super(LectureDetailView, self).form_invalid(form)


class CourseCreateView(CreateView):
    template_name='lecture/course_create.html'
    model = Course

    def get_success_url(self):
        return self.object.get_absolute_url()


class LectureCreateView(CreateView):
    template_name='lecture/lecture_create.html'
    model = Lecture
    form_class = LectureRegistratinForm

    def get_form_kwargs(self):
        kwargs = super(LectureCreateView, self).get_form_kwargs()
        if 'course' in self.request.GET:
            try:
                course = Course.objects.get(pk=self.request.GET['course'])
            except Course.DoesNotEsists:
                return kwargs
            kwargs.update({'initial': {'course': course}})
        return kwargs

    def get_success_url(self):
        return self.object.get_absolute_url()
