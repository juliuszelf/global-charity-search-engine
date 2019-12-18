#!/usr/bin/env python3
from __future__ import absolute_import

import sys

# Pycharm complains, but with absolute_import above it works.
from cleanCSV_parser import parse

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

# In seperate function for easier testing
parse(input_file_path, output_file_path)

