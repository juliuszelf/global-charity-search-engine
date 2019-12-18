from __future__ import absolute_import
import unittest
import os
# noinspection PyUnresolvedReferences
from cleanCSV_parser import parse


class CleanTestCase(unittest.TestCase):

    def setUp(self):
        # TODO remove when there is decent test
        print("setup ALWAYS TRUE TEST!")
        pass

    def tearDown(self):
        print("teardown")
        pass

    def test_head(self):
        # TODO: no xlsx test yet
        self.assertEqual(True, True)
