# -*- coding: utf-8 -*-
from django import forms

from .models import TestQuestion, TestQuestionVariant, LectureTest


class LectureTestForm(forms.Form):
    question_id_prefix = 'question'
    question_id_delimiter = '_'
    
    def __init__(self, test_info=None, *args, **kwargs):
        """test_info is a list with test questions.
           Example:
           [
            {'question_pk' : 23,
             'question' : '2 + 2 = ?',
             'variants' : [
               {1 : '1',
                2 : '4',
                3 : '8',
                4 : 'None'},
              ]
            },
            ...
           ]
        """
        super(LectureTestForm, self).__init__(*args, **kwargs)
        if test_info is not None:
            for question_info in test_info:
                field_name = self.get_field_name(question_info['question_pk'])
                question = question_info['question']
                answers = question_info['variants'].items()
                self.fields[field_name] = forms.ChoiceField(label=question, choices=answers, required=True)

    def clean(self):
        data = self.cleaned_data
        questions_pks = [self.extract_question_pk_from_field_name(f) for f in data.keys()]
        correct_answers = dict(TestQuestion.objects.filter(pk__in=questions_pks).values_list('pk', 'correct_answer_index'))
        for field_name, value in data.items():
            question_pk = self.extract_question_pk_from_field_name(field_name)
            if correct_answers[question_pk] != int(value):
                self._errors[field_name] = self.error_class(['Wrong!'])
        return data
    
    def get_field_name(self, question_pk):
        return '%s%s%s' % (self.question_id_prefix, self.question_id_delimiter, question_pk)

    def extract_question_pk_from_field_name(self, field_name):
        return int(field_name.split(self.question_id_delimiter)[1])
    
    @classmethod
    def get_lecture_test_form(cls, lecture_pk, data=None):
         test_info = LectureTest.get_lecture_test_info(lecture_pk)
         return LectureTestForm(test_info) if data is None else LectureTestForm(test_info, data)
