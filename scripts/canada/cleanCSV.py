#!/usr/bin/env python3

import sys
import csv
import json
from termcolor import colored

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

# First clean csv, we can then re-use the csvToJSON script for all datasets.
source_url = "https://open.canada.ca/data/en/dataset/7ef067c4-07a8-4882-ade3-643d00fd6c49"
source_date = "2016"

# we assume it data has heading like this:
"""
BN,Category,Designation,Legal Name,Account Name,Address Line 1,Address Line 2,City,Province,Postal Code,Country,Public Contact Name,Phone,Email,Website
"""
# For new file we are going to first rewrite the heading
# We keep: Legal Name, City, State, Country, Website
# We add: Source URL, Source date
end_part = source_url + "," + source_date + "\n" 

def fix_nulls(s):
    for line in s:
        yield line.replace('\0', ' ')

print("Opening output file..")
with open(output_file_path, 'w+', encoding="utf-8") as output_file:
     
    print("Write header..")
    fieldnames = ["Name", "City", "State", "Country", "Website", "SourceURL", "SourceDate"]
    output_writer = csv.DictWriter(output_file, 
                                    fieldnames=fieldnames, 
                                    delimiter=',', 
                                    quotechar='"', 
                                    quoting=csv.QUOTE_MINIMAL)
    output_writer.writeheader();

    # open to read source
    print("Opening source file..")

    with open(input_file_path, 'r') as input_file:

        input_reader = csv.DictReader(fix_nulls(input_file))

        # skip reading the first line with headers
        next(input_reader)

        for line in input_reader:
            output_writer.writerow({"Name": line["Legal Name"], 
                                    "City": line["City"], 
                                    "State": line["Province"], 
                                    "Country": line["Country"], 
                                    "Website": line["Website"], 
                                    "SourceURL": source_url, 
                                    "SourceDate": source_date})

# print first couple of lines as check
with open(output_file_path) as lines:
  print(colored("First two lines of created file:", 'green') )
  print(lines.readline(), end='')
  print(lines.readline(), end='')

print(colored("Ended cleaning CSV file", "green")) 

