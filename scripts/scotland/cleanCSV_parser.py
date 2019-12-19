#!/usr/bin/env python3

import sys
import csv
import json
from termcolor import colored

# First clean csv, we can then re-use the csvToJSON script for all datasets.
source_url = "https://www.oscr.org.uk/about-charities/search-the-register/charity-register-download"
source_date = "2019"  

# some of these are aliasses of other names also in the list
# Names from: https://www.geni.com/projects/Counties-of-Scotland-United-Kingdom/14402
counties = [
        "Aberdeenshire",
        "Angus",
        "Argyllshire",
        "Ayrshire",
        "Banffshire",
        "Moray council",
        "Aberdeenshire council",
        "Berwickshire",
        "Buteshire",
        "Caithness",
        "Clackmannanshire",
        "Dumfriesshire",
        "Dumfries",
        "Galloway)",
        "Dunbartonshire",
        "Lothian-Main-Page",
        "East Lothian",
        "Haddingtonshire",
        "Midlothian",
        "Fife/Fifeshire",
        "Inverness-shire",
        "Kincardineshire",
        "Kinross-shire",
        "Perth",
        "Kinross",
        "Kirkcudbrightshire",
        "Lanarkshire",
        "Linlithgowshire",
        "West Lothian",
        "Midlothian",
        "Edinburghshire",
        "Moray",
        "Morayshire",
        "Elginshire",
        "Nairnshire-Main-Page",
        "Nairn",
        "Nairnshire",
        "Highland",
        "Orkney",
        "Peebles-shire",
        "Borders",
        "Perthshire",
        "Perth",
        "Kinross",
        "Stirling",
        "Renfrewshire",
        "Ross and Cromarty",
        "Roxburghshire",
        "Selkirkshire",
        "Shetland",
        "Stirlingshire",
        "Sutherland",
        "West Lothian",
        "Linlithgowshire",
        "Wigtownshire"
    ]

# Categories from the 'purpose' field that have these values 
# will be placed in the generic category 'human'.
human_category_list = [
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
        "The advancement of health",
        ]

community_category_list = [
        "The advancement of citizenship or community development",
        "The prevention or relief of poverty",
        "The saving of lives",
        "The provision of recreational facilities, or the organisation of recreational activities, with the object of improving the conditions of life for the persons for whom the facilities or activities are primarily intended",
        "The advancement of human rights, conflict resolution or reconciliation",
        "The promotion of religious or racial harmony",
        "The promotion of equality and diversity",
        "The relief of those in need by reason of age, ill health, disability, financial hardship or other disadvantage",
        ]

religion_category_list = [
        "The advancement of religion",
        ]

culture_category_list = [
        "The advancement of the arts, heritage, culture or science",
        ]

sports_category_list = [
        "The advancement of public participation in sport",
        ]


def in_list(purpose, category_list):
    for cat in human_category_list:
        if cat in purr:
            return  1
    return 0


def get_category_values(purposes):
    # Using 0 as false, 1 as true
    # Because more compact in search engine (would otherwise write "True")

    # clean purpose from quotes
    pur = purposes.strip().replace("'", "")

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
    '''
    "Sports Pavilion, Pentcaitland, East Lothian"
    "The Old Garage, Mill Hills Farm, Crieff, Perthshire"
    "29A Westburn Drive, Aberdeen"
    "60 Brookfield Place, Alva, Clackmannanshire"
    "21 Church Street, Brechin, Angus"
    "Keppochan Farmhouse, Cladich, Dalmally"
    "Meeks Road Surgery, 10 Meeks Road, Falkirk"
    "24 Lanark Road, Edinburgh"
    "6 annerley court, cuparhead, coatbridge, lanarkshire"
    '''
    city = ""
    state = ""  # County / Shire
    parts = address.split(",")
    found_state = False
    # we 'reverse' parts, because we expect our values
    # to be within last 3 items.
    for part in reversed(parts):
        if not found_state:
            for county in counties:
                if part.strip() in county:
                    state = county.strip() 
                    found_state = True
        else:
            city = part.strip()
            return city, state

    # couldn't find county, lets assume city is last
    city = address.split(",")[-1].strip()
    return city, state


def fix_nulls(s):
    for line in s:
        yield line.replace('\0', ' ')


def parse(input_file_path, output_file_path):

    # we assume it data has heading like this:
    """
    Charity Number,
    Charity Name,
    Registered Date,
    Known As,
    Charity Status,
    Notes,
    Postcode,
    Constitutional Form,
    Previous Constitutional Form 1,
    Geographical Spread,
    Main Operating Location,
    Purposes,
    Beneficiaries,
    Activities,
    Objectives,
    Principal Office/Trustees Address,
    Website,
    Most recent year income,
    Most recent year expenditure,
    Mailing cycle,
    Year End,
    Donations and legacies income,
    Charitable activities income,
    Other trading activities income,
    Investments income,
    Other income,
    Raising funds spending,
    Charitable activities spending,
    Other spending,
    Parent charity name,
    Parent charity number,
    Parent charity country of registration,
    Designated religious body,
    Regulatory Type
    """
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
                city, state = get_values_from_address(line["Principal Office/Trustees Address"])
                human, nature, animal, education, health, community, religion, culture, sports = get_category_values(line["Purposes"])

                output_writer.writerow({"OfficialID": line["Charity Number"], 
                                        "Name": line["Charity Name"], 
                                        "City": city,
                                        "State": state, 
                                        "Country": "SC", 
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

