import unittest
from mock import patch
import sys


class CleanTestCase:

    def setUp(self):
        print("setup")
        pass

    def tearDown(self):
        print("teardown")
        pass

    def test_head(self):
	'''
	For 'canada': python3 scripts/canada/cleanCSV.py data/canada/rawutf8.csv data/canada/clean.csv
	'''
        # TODO: call python script 'from the outside', let it generate outcome
        source = 'data/n-ireland/testdata/raw.head.test.csv'
        output = 'data/n-ireland/testoutput/clean.csv'

        testargs = [source, output]

        with patch.object(sys, 'argv', testargs):
            setup = get_setup_file()
            assert setup == "/home/fenton/project/setup.py"

        # TODO: read outcome file, validate it's correct
        # TODO: clean up, remove outcome
        self.assertEqual(response.status_code, 200)
