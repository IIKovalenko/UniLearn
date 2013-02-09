# -*- coding: utf-8 -*-
from django import forms

from lecture.models import University, Course, Lecture, Lecturer, Student


class CourseRegistratinForm(forms.ModelForm):
    class Meta:
        model = Course


class LectureRegistratinForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if 'show_course_field' in kwargs:
            show_course_field = kwargs.pop('show_course_field')
        else:
            show_course_field = False
        super(LectureRegistratinForm, self).__init__(*args, **kwargs)
        if show_course_field:
            self.fields['course'].widget = forms.HiddenInput()
            
    class Meta:
        model = Lecture
