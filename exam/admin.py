from django.contrib import admin
from .models import TestQuestionVariant, TestQuestion, LectureTest


admin.site.register(LectureTest)
admin.site.register(TestQuestion)
admin.site.register(TestQuestionVariant)
