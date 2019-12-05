#!/usr/bin/env python3

import sys
import csv
import json
from termcolor import colored

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

# First clean csv, we can then re-use the csvToJSON script for all datasets.
source_url = "https://www.charitycommissionni.org.uk/charity-search/"
source_date = "2019"  # Not super sure about source date

# we assume it data has heading like this:
"""
Reg charity number,
Sub charity number,
Charity name,
Date registered,
Status,
Date for financial year ending,
Total income,
Total spending,
Charitable spending,
Income generation and governance,
Retained for future use,
Public address,
Website,
Email,
Telephone,
Company number,
What the charity does,
Who the charity helps,
How the charity works,
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
            # Adress is of form: "Supporting Communities Ni, 34-36 Henry Street, Ballymena, Co  Antrim, BT42 3AH"
            address = line["Public address"] 
            city = address.split(",")[-3]  # Takes "Ballymena" from example.
            state = address.split(",")[-2] 

            output_writer.writerow({"Name": line["Charity name"], 
                                    "City": city, 
                                    "State": state, 
                                    "Country": "GB-NIR", 
                                    "Website": line["Website"], 
                                    "SourceURL": source_url, 
                                    "SourceDate": source_date})

# print first couple of lines as check
with open(output_file_path) as lines:
  print(colored("First two lines of created file:", 'green') )
  print(lines.readline(), end='')
  print(lines.readline(), end='')

print(colored("Ended cleaning CSV file", "green")) 

