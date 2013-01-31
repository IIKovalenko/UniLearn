# -*- coding: utf-8 -*-
from django import forms

from .models import TestQuestion, TestQuestionVariant


class LectureTestForm(forms.Form):
    
   def __init__(self, test_info, *args, **kwargs):
       """test_info is a list with test questions.
          Example:
          [
           {'question' : '2 + 2 = ?',
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
       super(LectureTestForm, self).__init__(args, kwargs)
       for i, question_info in enumerate(test_info):
           field_name = 'question_%s' % i
           question = question_info['question']
           answers = question_info['variants'].items()
           self.fields[field_name] = forms.ChoiceField(label=question, choices=answers, required=True)

   @classmethod
   def get_lecture_test_form(cls, lecture_pk):
        questions = TestQuestion.objects.filter(test__lecture__pk=lecture_pk)
        questions_pks = [q.pk for q in questions]
        all_variants = list(TestQuestionVariant.objects.filter(pk__in=questions_pks))
        result = []
        for q in questions:
            question_info = {}
            question_info['question'] = q.text
            question_info['variants'] = {}
            this_questions_variants = filter(lambda v: v.question == q, all_variants)
            for variant in this_questions_variants:  #FIXME: simplify with dict compehansion
                question_info['variants'][variant.number] = variant.text
            result.append(question_info)
        return LectureTestForm(result)
