from django.test import TestCase
from django.core.urlresolvers import reverse
from operator import attrgetter

from account.models import UserProfile
from lecture.models import Course, Lecture
from lecture.factories import CourseFactory, LectureFactory


class LecturesTest(TestCase):
    def create_and_login_user(self):
        login, password = 'test_user', 'pwd'
        self.user = UserProfile.objects.create_user(login, 'test@user.com', password)
        self.client.login(username=login, password=password)

    def setUp(self):
        self.courses_amount = 5
        self.lectures_amount = 5
        self.courses = [CourseFactory() for _ in xrange(self.courses_amount)]
        for course in self.courses:
            [LectureFactory(course=course) for _ in xrange(self.lectures_amount)]
        self.course = self.courses[0]
        self.create_and_login_user()

    def test_course_list_shows_all_courses(self):
        response = self.client.get(reverse('course-list'))
        all_courses_pks = [c.pk for c in Course.objects.all()]
        self.assertQuerysetEqual(response.context['courses'], all_courses_pks, transform=attrgetter('pk'))

    def test_course_has_lecture_list(self):
        course_lectures_pks = [l.pk for l in Lecture.objects.filter(course=self.course)]
        response = self.client.get(reverse('course-detail', args=(self.course.pk, )))
        self.assertQuerysetEqual(response.context['lectures'], course_lectures_pks, transform=attrgetter('pk'))        

    def test_lecture_has_text_and_title(self):
        lecture = Lecture.objects.filter(course=self.course)[0]
        response = self.client.get(reverse('lecture-detail', args=(lecture.course.pk, lecture.number)))
        self.assertContains(response, lecture.title)
        self.assertContains(response, lecture.text)        


class LectureAddPageTest(TestCase):
    def create_and_login_user(self):
        login, password = 'test_user', 'pwd'
        self.user = UserProfile.objects.create_user(login, 'test@user.com', password)
        self.client.login(username=login, password=password)

    def setUp(self):
        self.course = CourseFactory()
        self.create_and_login_user()

    def test_course_field_shows_up_by_default(self):
        response = self.client.get(reverse('lecture-add'))
        self.assertFalse(response.context['form'].fields['course'].widget.is_hidden)

    def test_course_field_hidden_with_initial_when_course_specified(self):
        response = self.client.get('%s?course=%s' % (reverse('lecture-add'), self.course.pk))
        self.assertTrue(response.context['form'].fields['course'].widget.is_hidden)
        self.assertEqual(response.context['form'].initial['course'].pk, self.course.pk)
