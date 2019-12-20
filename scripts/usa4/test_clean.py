from __future__ import absolute_import
import unittest
import os
# noinspection PyUnresolvedReferences
from cleanCSV_parser import parse


class CleanTestCase(unittest.TestCase):

    def setUp(self):
        print("setup")
        pass

    def tearDown(self):
        print("teardown")
        pass

    def test_head(self):
        print("NO TEST")
        '''
        source = 'testdata/raw.head.test.csv'
        output = 'testoutput/clean.head.csv'
        expected = 'testdata/clean.head.expected.csv'

        parse(source, output)

        # Now we should have created a file, validate it is equal to expected result.
        with open(output) as f:
            content_output = f.read()

        with open(expected) as f:
            expected_output = f.read()

        self.assertEqual(expected_output, content_output)

        # cleanup
        os.remove(output)
        '''
