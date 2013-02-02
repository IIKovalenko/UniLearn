# -*- coding: utf-8 -*-
from django.test.testcases import TestCase
from django.core import management
import logging

class MakefishdataTest(TestCase):

    def test_makefishdata(self):
        management.call_command('make_fish_data', verbosity=0, interactive=False)
