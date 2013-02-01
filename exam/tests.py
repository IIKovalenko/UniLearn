from django.test import TestCase

from lecture.models import Lecture
from .factories import TestQuestionFactory, TestQuestionVariantFactory, LectureTestFactory
from .forms import LectureTestForm
from .models import TestQuestionVariant


class LectureTestFormTest(TestCase):
    def setUp(self):
        self.questions_amount = 2
        self.each_question_variants_amount = 3
        self.test = LectureTestFactory()
        self.questions = [TestQuestionFactory(test=self.test) for _ in xrange(self.questions_amount)]
        for q in self.questions:
            created_variants_numbers = [TestQuestionVariantFactory(question=q).number for _ in xrange(self.each_question_variants_amount - 1)]
            if not q.correct_answer_index in created_variants_numbers:
                TestQuestionVariantFactory(question=q, number=q.correct_answer_index)
            else:
                TestQuestionVariantFactory(question=q)                
        self.lecture = Lecture.objects.all()[0]

    def __get_correct_data(self, form):
        correct_data = {}
        for q in self.questions:
            field_name = form.get_field_name(q.pk)
            correct_data[field_name] = q.correct_answer_index
        return correct_data

    def __get_incorrect_data(self, form):
        incorrect_data = {}
        for q in self.questions:
            field_name = form.get_field_name(q.pk)
            incorrect_variants = dict(form.fields[field_name].choices).keys()
            incorrect_variants.remove(q.correct_answer_index)
            incorrect_data[field_name] = incorrect_variants[0]
        return incorrect_data

    def test_form_class_creates_form_by_pk(self):
        form = LectureTestForm.get_lecture_test_form(self.lecture.pk)
        self.assertTrue(type(form) == LectureTestForm)

    def test_created_form_has_field_for_each_question(self):
        form = LectureTestForm.get_lecture_test_form(self.lecture.pk)
        fields_amount = len(form.fields)
        self.assertEqual(fields_amount, self.questions_amount)

    def test_form_fields_has_right_pks(self):
        form = LectureTestForm.get_lecture_test_form(self.lecture.pk)        
        questions_pks = [q.pk for q in self.questions]
        actual_pks = [int(f.split(form.question_id_delimiter)[1]) for f in form.fields]
        self.assertListEqual(questions_pks, actual_pks)

    def test_created_form_has_choices_with_correct_variants(self):
        form = LectureTestForm.get_lecture_test_form(self.lecture.pk)
        for field in form.fields.values():
            choices_amount = len(field.choices)
            self.assertEqual(choices_amount, self.each_question_variants_amount)

    def __test_raises_exceptions_if_correct_indexes_not_in_variants(self):
        test_question = self.questions[0]
        correct_answer = TestQuestionVariant.objects.filter(question=test_question, number=test_question.correct_answer_index)
#        correct_answer.delete() # DatabaseError: no such table: nose_c - WTF?
        form = None #FIXME self.assertRaises
        try:
            form = LectureTestForm.get_lecture_test_form(self.lecture.pk)
        except ValueError:
            pass
        self.assertTrue(form == None)

    def __test_form_validates_if_data_correct(self):
        form = LectureTestForm.get_lecture_test_form(self.lecture.pk)
        correct_data = self.__get_correct_data(form)
        self.assertTrue(form(correct_data).is_valid())

    def test_form_fails_if_data_incorrect(self):
        form = LectureTestForm.get_lecture_test_form(self.lecture.pk)
        incorrect_data = self.__get_incorrect_data(form)
        bounded_form = LectureTestForm.get_lecture_test_form(lecture_pk=self.lecture.pk, data=incorrect_data)
        self.assertFalse(bounded_form.is_valid())
