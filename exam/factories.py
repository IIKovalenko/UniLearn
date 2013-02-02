import factory

from .models import TestQuestionVariant, TestQuestion, LectureTest
from lecture.factories import LectureFactory

class LectureTestFactory(factory.Factory):
    FACTORY_FOR = LectureTest

    lecture = factory.SubFactory(LectureFactory)

    @factory.post_generation()
    def questions(self, create, extracted, **kwargs):    
        if extracted:
            [TestQuestionFactory(test=self, variants=True) for _ in xrange(extracted)]
                

class TestQuestionFactory(factory.Factory):
    FACTORY_FOR = TestQuestion

    test = factory.SubFactory(LectureTestFactory)
    question = factory.Sequence(lambda n: ' Test question %s' % n)
    type = 'FV'
    correct_answer_index = factory.Sequence(lambda n: int(n))

    @factory.post_generation()
    def variants(self, create, extracted, **kwargs):
        variants_amount = 5
        if extracted:
            [TestQuestionVariantFactory(question=self) for _ in xrange(variants_amount)]


class TestQuestionVariantFactory(factory.Factory):
    FACTORY_FOR = TestQuestionVariant

    question = factory.SubFactory(TestQuestionFactory)
    text = factory.Sequence(lambda n: 'Test variant %s' % n)
    number = factory.Sequence(lambda n: int(n))
