#!/usr/bin/env python3

import csv
from termcolor import colored

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

human_category_list = [
        "Other charitable purposes",
        ]

nature_category_list = [
        "The advancement of environmental protection or improvement",
        ]

animal_category_list = [
        "The advancement of animal welfare"
        ]

education_category_list = [
        "The advancement of education",
        ]

health_category_list = [
        "The advancement of health or the saving of lives",
        ]

community_category_list = [
        "The advancement of citizenship or community development",
        "The relief of those in need by reason of youth, age, ill-health, disability, financial hardship or other disadvantage",
        "The prevention or relief of poverty",
        "The advancement of human rights, conflict resolution or reconciliation or the promotion of religious or racial harmony or equality and diversity",
        ]

religion_category_list = [
        "The advancement of religion",
        ]

culture_category_list = [
        "The advancement of the arts, culture, heritage or science",

        ]

sports_category_list = [
        "The advancement of amateur sport"
        ]

counties = [
        'Antrim',
        'Armagh',
        'Down',
        'Fermanagh',
        'Londonderry',
        'Tyrone'
        ]


def in_list(purpose, category_list):
    """
    The ugly part is that te different catories are comma seperated, but each category label also can have commas.
    So we can't really split 'purpose', so we simple test if a category label is 'in' the 'purpose'.
    """
    for cat in category_list:
        if cat in purpose:
            return 1
    else:
        return 0


def get_category_values(purposes):

    # clean purpose from quotes
    pur = purposes.strip().replace("'", "")

    # Receives value 0 as false, 1 as true
    # Because more compact in search engine (would otherwise write "True")
    human = in_list(pur, human_category_list)
    nature = in_list(pur, nature_category_list)
    animal = in_list(pur, animal_category_list)
    education = in_list(pur, education_category_list)
    health = in_list(pur, health_category_list)
    community = in_list(pur, community_category_list)
    religion = in_list(pur, religion_category_list)
    culture = in_list(pur, culture_category_list)
    sports = in_list(pur, sports_category_list)

    return human, nature, animal, education, health, community, religion, culture, sports


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


def parse(input_file_path, output_file_path):

    # For new file we are going to first rewrite the heading
    # We keep: Legal Name, City, State, Country, Website
    # We add: Source URL, Source date
    end_part = source_url + "," + source_date + "\n" 

    print("Opening output file..")
    with open(output_file_path, 'w+', encoding="utf-8") as output_file:
        
        print("Write header..")
        fieldnames = [
                "OfficialID", 
                "Name", 
                "City", 
                "State", 
                "Country", 
                "Website",
                "HUM", 
                "NAT", 
                "ANI", 
                "EDU", 
                "HEA", 
                "COM", 
                "REL", 
                "CUL", 
                "SPO", 
                "SourceURL", 
                "SourceDate"
                ]
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

            for line in input_reader:
                # Adress is of form: "Supporting Communities Ni, 34-36 Henry Street, Ballymena, Co  Antrim, BT42 3AH"
                address = line["Public address"] 
                city, state = get_values_from_address(address)
                human, nature, animal, education, health, community, religion, culture, sports = get_category_values(line["What the charity does"])

                output_writer.writerow({"OfficialID": line["Reg charity number"],
                                        "Name": line["Charity name"], 
                                        "City": city, 
                                        "State": state, 
                                        "Country": "GB-NIR", 
                                        "Website": line["Website"], 
                                        "HUM": human, 
                                        "NAT": nature, 
                                        "ANI": animal, 
                                        "EDU": education, 
                                        "HEA": health, 
                                        "COM": community, 
                                        "REL": religion, 
                                        "CUL": culture, 
                                        "SPO": sports, 
                                        "SourceURL": source_url, 
                                        "SourceDate": source_date})

    # print first couple of lines as check
    with open(output_file_path) as lines:
        print(colored("First two lines of created file:", 'green') )
        print(lines.readline(), end='')
        print(lines.readline(), end='')

    print(colored("Ended cleaning CSV file", "green")) 

