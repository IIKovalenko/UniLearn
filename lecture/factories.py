import factory

from lecture.models import University, Course, Lecture, Lecturer, Student

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


class StudentFactory(factory.Factory):
    FACTORY_FOR = Student

    full_name = 'Grigori Yakovlevich Perelman'
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

    @classmethod
    def _prepare(cls, create, **kwargs):
        lecture = super(LectureFactory, cls)._prepare(create, **kwargs)
        designers_amount = 5
        for _ in xrange(designers_amount):
            lecture.designers.add(StudentFactory())
        return lecture


class LecturerFactory(factory.Factory):
    FACTORY_FOR = Lecturer

    full_name = 'Richard Feynman'
    university = factory.SubFactory(UniversityFactory)
