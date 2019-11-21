#!/usr/bin/env python3

"""
Script to convert a .csv file to a .json file that can be bulk uploaded to elasticsearch with curl. 

Assumes .csv file with "c" seperator.
Spaces wil not be trimmed. So best is to clean .csv file beforehand.
"""

import csv
import json
import sys
from termcolor import colored

default_country_name = "canada"
default_output_file = "data.es.json"
default_index = "data"

if len(sys.argv[1]) == 0:
    # Ask input file
    country_name = input(colored("country folder name: ", "yellow"))

    if country_name == "":
      country_name = default_country_name
else:
    # Variable passed to script
    country_name = sys.argv[1]
    print("Country name provided: " + country_name)

# Infer output file
input_file = "../data/" + country_name + "/" + country_name + ".clean.csv"
output_file = "../data/" + country_name + "/" + country_name + ".es.json"

if len(sys.argv[2]) == 0:
    # Ask index (elastic search index is the name of the 'table')
    index_name = input(colored("index name: (default '" + default_index + "'): ", "yellow"))

    if index_name == "":
      index_name = default_index
else:
    # Variable passed to script
    index_name = sys.argv[2]
    print("Index name provided: " + index_name)


# Convert to JSON

# open to read source
print("Opening source file..")
f = open(input_file, 'r', encoding="utf-8")
reader = csv.DictReader(f)

# Every other json line needs to state the index for bulk upload
# No id is given, so will be random
index_line = '{"index" : { "_index" : "' + index_name + '"}}\n'

# open output and write json
print("Opening output file..")
with open(output_file, 'w+', encoding="utf-8") as of:
    for x in reader:
        of.write(index_line)
        json.dump(x, of, ensure_ascii=False)
        of.write("\n")

f.close()

print("json file created. First 2 lines of file read: ")

with open(output_file) as lines:
  print(colored(lines.readline(), 'white'), end='')
  print(colored(lines.readline(), 'white'))

print(colored("Ended converting CSV file '" + input_file + "' to JSON in '" + output_file + "', placed in index '" + index_name+ "'.", "green")) 


