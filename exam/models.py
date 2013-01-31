from django.db import models


class LectureTest(models.Model):
    lecture = models.OneToOneField('lecture.Lecture', related_name='test')

    def __unicode__(self):
        return 'Test for lecture %s' % self.lecture


class TestQuestion(models.Model):
    QUESION_TYPES = {
        'FV' : 'Question with fixed variants',
        'FA' : 'Qustion with free form of answer'
    }
    QUESION_DIFFICULTIES = {
        1 : 'Easy question',        
        2 : 'Question of middle difficulty',
        3 : 'Difficult question',
    }
    
    test = models.ForeignKey('LectureTest', related_name='questions')
    question = models.CharField(max_length=1023)
    type = models.CharField(max_length=2, choices=QUESION_TYPES.items(), default='FV')
    correct_answer_index = models.SmallIntegerField('Number of correct variant', blank=True, null=True)
    correct_answer_text = models.CharField('Correct answer for question with free form', max_length=511, blank=True)
    difficulty = models.SmallIntegerField(max_length=1, choices=QUESION_DIFFICULTIES.items(), default=2)

    def __unicode__(self):
        return self.question


class TestQuestionVariant(models.Model):
    question = models.ForeignKey('TestQuestion', related_name='variants')
    text = models.CharField(max_length=1023)
    number = models.SmallIntegerField()

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ('question', 'number')
