from django.contrib import admin
from lecture.models import University, Course, Lecture, Lecturer, Student

admin.site.register(University)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Lecturer)
admin.site.register(Student)
