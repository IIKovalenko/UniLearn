from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

import factory as factory_module

from lecture.models import Student
from lecture.factories import UniversityFactory, CourseFactory, StudentFactory, LectureFactory, LecturerFactory
from exam.factories import LectureTestFactory, TestQuestionFactory, TestQuestionVariantFactory


class Command(BaseCommand):
    help = 'Generate test database data'

    option_list = BaseCommand.option_list + (
        make_option('--clear',
            action='store_true',
            dest='clear',
            default=False,
            help='Clear all tables before generating data'),
        )
    factory_list = [
        (CourseFactory, 3, {'lectures' : 10}),
    ]

    # Additional models to be cleared.
    # Models wich are FACORY_FOR and models with relationships
    # with them will be cleared automatically (with --clear key)
    additional_models = [
        Student,
    ]

    def _get_models_list(self):
        models = []
        for f in self.factory_list:
            models +=self._get_factory_models(f[0])
        return set(models + self.additional_models)

    def _get_factory_models(self, factory):
        """Get models list which instances can de created with factory.
           Falls into infinite recursion if there are symmetric SubFactories.
        """
        factory_for_model = factory._associated_class
        models = [factory_for_model]
        for field_name, generator_object in factory._declarations.items():
            if type(generator_object) == factory_module.declarations.SubFactory:
                field_factory = generator_object.factory
                models += self._get_factory_models(field_factory)
        return models

    def _clear_database(self):
        for model in self._get_models_list():
            model.objects.all().delete()
    
    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Cleaning database...')
            self._clear_database()
            self.stdout.write('finished!')
        self.stdout.write('Creating model instances...')
        for factory_class, call_amounts, factory_arguments in self.factory_list:
            [factory_class(**factory_arguments) for _ in xrange(call_amounts)]
        self.stdout.write('finished!')
