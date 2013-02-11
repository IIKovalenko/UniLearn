from django.db import models

from ckeditor.fields import HTMLField


class University(models.Model):
    name = models.CharField('Name', max_length=100)
    abbrev = models.CharField('Abbreviation',max_length=10)

    class Meta:
        ordering = ('name',)
        verbose_name = 'University'
        verbose_name_plural = 'Universities'

    def __unicode__(self):
	return self.abbrev


class Course(models.Model):
    title = models.CharField('Title', max_length=100, unique=True)
    abbrev = models.CharField('Abbreviation', max_length=10, unique=True)
    prerequsites = models.TextField('Prerequisites')
    description = models.TextField('Description')

    class Meta:
        ordering = ("title",)
        verbose_name = u"Course"
        verbose_name_plural = u"Courses"

    def __unicode__(self):
	return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'course-detail', (self.pk,), {}


class Lecturer(models.Model):
    full_name = models.CharField('Full name', max_length=200)
    university = models.ForeignKey('University', related_name='lecturers', verbose_name='University', null=True, blank=True)
    courses = models.ManyToManyField(Course, verbose_name='Courses', null=True, blank=True)

    class Meta:
        ordering = ("full_name",)
        verbose_name = u"Lecturer"
        verbose_name_plural = u"Lecturers"

    def __unicode__(self):
	return self.title


class Student(models.Model):
    full_name = models.CharField('Full name', max_length=200)
    university = models.ForeignKey('University', verbose_name='University')
    curriculum = models.PositiveIntegerField('Curriculum')
    group_abbrev = models.CharField('Group abbreviation', max_length=10)    

    class Meta:
        ordering = ("curriculum", "group_abbrev", "full_name")
        verbose_name = u"Student"
        verbose_name_plural = u"Students"

    def __unicode__(self):
        return u"%s"%(self.full_name)
    

class Lecture(models.Model):
    title = models.CharField('Title', max_length=100)
    course = models.ForeignKey('Course', related_name='courses')
    number = models.PositiveIntegerField()
    basic_concepts = models.CharField(max_length=300, null=True, blank=True)
    designers = models.ManyToManyField(Student)
    text = HTMLField()

    class Meta:
        ordering = ("course", "number")
        verbose_name = u"Lecture"
        verbose_name_plural = u"Lectures"

    def __unicode__(self):
       	return "[%s]%s"%(self.course, self.title)

    @models.permalink
    def get_absolute_url(self):
        return 'lecture-detail', (), {'course_pk': self.course.pk, 'lecture_num': self.number}
