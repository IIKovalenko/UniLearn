from django.db import models

from model_utils import Choices


class LectureTest(models.Model):
    lecture = models.OneToOneField('lecture.Lecture', related_name='test')

    def __unicode__(self):
        return 'Test for lecture %s' % self.lecture

    @classmethod
    def get_lecture_test_info(cls, lecture_pk):
        """Return list with info about questions and variants for creating LectureTestForm."""
        questions = TestQuestion.objects.filter(test__lecture__pk=lecture_pk)

        questions_pks = [q.pk for q in questions]
        all_variants = list(TestQuestionVariant.objects.filter(question__pk__in=questions_pks))
        result = []
        for q in questions:
            question_info = {}
            question_info['question_pk'] = q.pk
            question_info['question'] = q.question
            question_info['variants'] = {}
            this_questions_variants = filter(lambda v: v.question == q, all_variants)
            for variant in this_questions_variants:  #FIXME: simplify with dict compehansion
                question_info['variants'][variant.number] = variant.text
            result.append(question_info)
        return result
     

class TestQuestion(models.Model):
    QUESTION_TYPES = Choices(
        ('FV', 'fixed_variants', 'Question with fixed variants'),
        ('FA', 'free_form', 'Qustion with free form of answer')
    )
    QUESTION_DIFFICULTIES = Choices(
        (1, 'easy', 'Easy question'),
        (2, 'middle', 'Question of middle difficulty'),
        (3, 'difficult', 'Difficult question')
    )
   
    test = models.ForeignKey('LectureTest', related_name='questions')
    question = models.CharField(max_length=1023)
    type = models.CharField(max_length=2, choices=QUESTION_TYPES, default=QUESTION_TYPES.fixed_variants)
    correct_answer_index = models.SmallIntegerField('Number of correct variant', blank=True, null=True)
    correct_answer_text = models.CharField('Correct answer for question with free form', max_length=511, blank=True)
    difficulty = models.SmallIntegerField(max_length=1, choices=QUESTION_DIFFICULTIES, default=QUESTION_DIFFICULTIES.middle)

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
