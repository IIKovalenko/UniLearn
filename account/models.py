from django.db import models
from django.contrib.auth.models import AbstractUser

from model_utils import Choices

from lecture.models import Lecture

 
class UserProfile(AbstractUser):

    def _update_profile_statistics(self, lecture_pk, new_status):
        stat = self.get_lecture_status(lecture_pk)
        if stat.status_can_be_changed_to(new_status):
            stat.status = new_status
            stat.save()

    def read_lecture(self, lecture_pk):
        self._update_profile_statistics(lecture_pk, UserTestStatistics.TEST_STATUSES.not_passed)

    def passed_test(self, lecture_pk):
        self._update_profile_statistics(lecture_pk, UserTestStatistics.TEST_STATUSES.passed)

    def failed_test(self, lecture_pk):
        self._update_profile_statistics(lecture_pk, UserTestStatistics.TEST_STATUSES.failed)

    def get_lecture_status(self, lecture_pk):
        try:
            stat = UserTestStatistics.objects.get(user=self, lecture__pk=lecture_pk)
        except UserTestStatistics.DoesNotExist:
            lecture = Lecture.objects.get(pk=lecture_pk)
            stat = UserTestStatistics.objects.create(user=self, lecture=lecture) # with default status
        return stat

        

class UserTestStatistics(models.Model):
    TEST_STATUSES = Choices(
        ('NR', 'not_readed', 'Lecture hasn\'t been readed'),
        ('NP', 'not_passed', 'Lecture\'s test hasn\'t been passed'),
        ('FL', 'failed', 'Lecture\'s test has been failed'),
        ('PD', 'passed', 'Lecture\'s test has been passed'),        
    )
    POSSIBLE_STATUSES_TRANSFORMATIONS = {
        'NR': ('NP', ),
        'NP': ('FL', 'PD', ),
        'FL': ('PD', ),
        'PD': (),
    }
    user = models.ForeignKey(UserProfile)
    lecture = models.ForeignKey(Lecture)
    status = models.CharField(choices=TEST_STATUSES, default=TEST_STATUSES.not_readed, max_length=2)

    def status_can_be_changed_to(self, new_status):
        return new_status in UserTestStatistics.POSSIBLE_STATUSES_TRANSFORMATIONS[self.status]
    
    def __unicode__(self):
	return self.status
