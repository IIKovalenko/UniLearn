from django.core.urlresolvers import reverse
from operator import attrgetter

from unilearn.tests import AutoLoginTestCase
from account.models import UserProfile, UserTestStatistics
from lecture.models import Course, Lecture
from lecture.factories import CourseFactory, LectureFactory


class LecturesTest(AutoLoginTestCase):
    def setUp(self):
        super(LecturesTest, self).setUp()
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


class LectureAddPageTest(AutoLoginTestCase):
    def setUp(self):
        super(LectureAddPageTest, self).setUp()
        self.course = CourseFactory()
        self.create_and_login_user()

    def test_course_field_shows_up_by_default(self):
        response = self.client.get(reverse('lecture-add'))
        self.assertFalse(response.context['form'].fields['course'].widget.is_hidden)

    def test_course_field_hidden_with_initial_when_course_specified(self):
        response = self.client.get('%s?course=%s' % (reverse('lecture-add'), self.course.pk))
        self.assertTrue(response.context['form'].fields['course'].widget.is_hidden)
        self.assertEqual(response.context['form'].initial['course'].pk, self.course.pk)

class LectureStatusTest(AutoLoginTestCase):
    def setUp(self):
        super(LectureStatusTest, self).setUp()
        self.course = CourseFactory()
        self.lecture = LectureFactory(course=self.course, test=True)
        self.lecture_url = reverse('lecture-detail', args=(self.course.pk, self.lecture.number))
        self.create_and_login_user()

    def test_default_status_is_not_readed(self):
        actual_default_status = self.user.get_lecture_status(self.lecture.pk).status
        expected_default_status = UserTestStatistics.TEST_STATUSES.not_readed
        self.assertEqual(actual_default_status, expected_default_status)

    def test_lecture_marks_as_not_passed_when_opened(self):
        response = self.client.get(self.lecture_url)
        actual_status = self.user.get_lecture_status(self.lecture.pk).status
        expected_status = UserTestStatistics.TEST_STATUSES.not_passed
        self.assertEqual(actual_status, expected_status)

    def test_lecture_marks_as_failed_when_test_fails(self):
        response = self.client.get(self.lecture_url)
        response = self.client.post(self.lecture_url,data={})
        actual_status = self.user.get_lecture_status(self.lecture.pk).status
        expected_status = UserTestStatistics.TEST_STATUSES.failed
        self.assertEqual(actual_status, expected_status)
