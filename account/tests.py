from django.core.urlresolvers import reverse

from unilearn.tests import AutoLoginTestCase
from .models import UserTestStatistics, UserProfile
from lecture.models import Course, Lecture
from lecture.factories import CourseFactory, LectureFactory


class LecturesStatisticsTest(AutoLoginTestCase):

    def setUp(self):
        super(LecturesStatisticsTest, self).setUp()
        self.courses_amount = 5
        self.lectures_amount = 5
        self.courses = [CourseFactory() for _ in xrange(self.courses_amount)]
        for course in self.courses:
            [LectureFactory(course=course, test=True) for _ in xrange(self.lectures_amount)]
        self.course = self.courses[0]
        self.lecture = Lecture.objects.filter(course=self.course)[0]
        self.create_and_login_user()
        
    def test_status_changed_when_opened_lecture(self):
        response = self.client.get(reverse('lecture-detail', args=(self.course.pk, self.lecture.number)))
        lecture_status = self.user.get_lecture_status(self.lecture.pk)
        self.assertEqual(lecture_status.status, UserTestStatistics.TEST_STATUSES.not_passed)

    def test_has_default_status_for_new_lecture(self):
        lecture_status = self.user.get_lecture_status(self.lecture.pk)
        self.assertEqual(lecture_status.status, UserTestStatistics.TEST_STATUSES.not_readed)
