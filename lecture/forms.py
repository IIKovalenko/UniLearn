# -*- coding: utf-8 -*-
from django import forms

from lecture.models import University, Course, Lecture, Lecturer, Student


class CourseRegistratinForm(forms.ModelForm):
    class Meta:
        model = Course