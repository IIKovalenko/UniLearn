from random import random

import factory

from .models import University, Course, Lecture, Lecturer, Student


class UniversityFactory(factory.Factory):
    FACTORY_FOR = University

    name = 'Bauman Moscow State Technical University'
    abbrev = 'BMSTU'


class CourseFactory(factory.Factory):
    FACTORY_FOR = Course

    title = factory.Sequence(lambda n: 'Machine Learning %s' % n)
    abbrev = factory.Sequence(lambda n: 'ML-%s' % n)
    prerequsites = 'Basic math'
    description = 'Basic ML problems and methods overview'

    @factory.post_generation()
    def lectures(self, create, extracted, **kwargs):    
        if extracted:
            [LectureFactory(course=self, test=True) for _ in xrange(extracted)]

            
class StudentFactory(factory.Factory):
    FACTORY_FOR = Student

    full_name = factory.Sequence(lambda n: 'Grigori Yakovlevich Perelman %s' % n)
    university = factory.SubFactory(UniversityFactory)
    curriculum = factory.Sequence(lambda n: n)
    group_abbrev = factory.Sequence(lambda n: 'AK-%s' % n)


class LectureFactory(factory.Factory):
    FACTORY_FOR = Lecture

    title = factory.Sequence(lambda n: 'Lecture %s' % n)
    course = factory.SubFactory(CourseFactory)
    number = factory.Sequence(lambda n: n)
    basic_concepts = 'concrete basic concepts'
    text = factory.Sequence(lambda n: 'concrete lecture body %s' % n)

    @factory.post_generation()
    def test(self, create, extracted, **kwargs):
        from exam.factories import LectureTestFactory  # to avoid recursive imports
        if extracted:
            LectureTestFactory(lecture=self, questions=5)

    @factory.post_generation()
    def designers(self, create, extracted, **kwargs):
        designers_amount = 5
        [self.designers.add(StudentFactory()) for _ in xrange(designers_amount)]
        

class LecturerFactory(factory.Factory):
    FACTORY_FOR = Lecturer

    full_name = 'Richard Feynman'
    university = factory.SubFactory(UniversityFactory)
