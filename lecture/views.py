from django.views.generic import ListView
from django.views.generic.detail import DetailView

from lecture.models import Course


class CoursesListView(ListView):
    model = Course
    template_name='lecture/course_list.html'
    context_object_name = 'courses'
