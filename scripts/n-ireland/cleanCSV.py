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

# Categories from the 'what charity does' field that have these values 
# will be placed in the generic category 'human'.
human_category_list = [
        "The advancement of education",
        "The advancement of religion",
        "The advancement of health or the saving of lives",
        "The advancement of citizenship or community development",
        "The relief of those in need by reason of youth, age, ill-health, disability, financial hardship or other disadvantage",
        "The prevention or relief of poverty",
        "The advancement of the arts, culture, heritage or science",
        "The advancement of human rights, conflict resolution or reconciliation or the promotion of religious or racial harmony or equality and diversity",
        "Other charitable purposes",
        "The advancement of amateur sport"
        ]

nature_category_list = [
        "The advancement of environmental protection or improvement",
        "The advancement of animal welfare"
        ]

# Same function as for Scotland
def get_category_values(purposes):
    # Using 0 as false, 1 as true
    # Because more compact in search engine (would otherwise write "True")
    human = 0 
    nature = 0 

    # clean purpose from quotes
    pur = purposes.strip().replace("'", "")

    # Assumption is that purpose field is mutually exclusive,
    # so charity can only have sigle purpose
    # TODO: check from raw data if this is correct,
    # the fact that it's multiple purposeS is suspect.
    if pur in human_category_list:
        human = 1

    if pur in nature_category_list:
        nature = 1
    
    return human, nature

counties = [
        'Antrim',
        'Armagh',
        'Down',
        'Fermanagh',
        'Londonderry',
        'Tyrone'
        ]

def get_values_from_address(address):

    # There is a single field "Address" in the CSV, this holds values like:
    '''
    "Ballygasey Road, 	Loughgall, 	Armagh, 	BT61 8HY"
    "29 Main Street, 	Clough, 	Downpatrick, 	Co.Down, N.Ireland, BT30 8RA"
    "34B Barra Drive, 	Ballymena, 	BT42 4AH"
    "50 Granemore Park, Keady, 		Armagh, 	BT60 2GP"
    "6 Harmony Mews, 	Lisburn, 	BT27 4EG"
    "70 Prince Andrew Way, 	Carrickfergus, 	BT38 7TB"
    "Young Enterprise N I, 	Grove House, 	145-149 Donegall Pass, Belfast, BT7 1DT"
    '''
    # The trouble is that there is no fixed format
    # To get the county (will go to field 'state', we'll check against this list:
    # The next challenge is that it often, but not always includes the word 'county'.
    # The rule I'm going with is '
    parts = address.split(",")
    city = ""
    state = ""  # County

    found_state = False
    # we 'reverse' parts, because we expect our values
    # to be within last 3 items.
    for part in reversed(parts):
        if not found_state:
            for county in counties:
                if county in part:
                    state = county.strip() 
                    found_state = True
            
        else:
          city = part.strip()
          return city, state
    # couldn't find county, lets assume city is before last
    # We assume the city is the value before the state
    # Or the value maching any of the top 10 cities
    # Or if the value before the last.
    city = address.split(",")[-2].strip()
    return city, state

def fix_nulls(s):
    for line in s:
        yield line.replace('\0', ' ')

print("Opening output file..")
with open(output_file_path, 'w+', encoding="utf-8") as output_file:
     
    print("Write header..")
    fieldnames = ["Name", "City", "State", "Country", "Website","HUM", "NAT", "SourceURL", "SourceDate"]
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
            city, state = get_values_from_address(address)
            human, nature = get_category_values(line["What the charity does"])

            output_writer.writerow({"Name": line["Charity name"], 
                                    "City": city, 
                                    "State": state, 
                                    "Country": "GB-NIR", 
                                    "Website": line["Website"], 
                                    "HUM": human, 
                                    "NAT": nature, 
                                    "SourceURL": source_url, 
                                    "SourceDate": source_date})

# print first couple of lines as check
with open(output_file_path) as lines:
  print(colored("First two lines of created file:", 'green') )
  print(lines.readline(), end='')
  print(lines.readline(), end='')

print(colored("Ended cleaning CSV file", "green")) 

