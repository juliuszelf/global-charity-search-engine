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
        "The prevention or relief of poverty",
        "The advancement of education",
        "The advancement of religion",
        "The advancement of health",
        "The saving of lives",
        "The advancement of citizenship or community development",
        "The advancement of the arts, heritage, culture or science",
        "The advancement of public participation in sport",
        "The provision of recreational facilities, or the organisation of recreational activities, with the object of improving the conditions of life for the persons for whom the facilities or activities are primarily intended",
        "The advancement of human rights, conflict resolution or reconciliation",
        "The promotion of religious or racial harmony",
        "The promotion of equality and diversity",
        "The relief of those in need by reason of age, ill health, disability, financial hardship or other disadvantage",
        ]

nature_category_list = [
        "The advancement of environmental protection or improvement",
        ]

animal_category_list = [
        "The advancement of animal welfare"
        ]


# Same function as for Australia
def get_category_values(purposes):
    # Using 0 as false, 1 as true
    # Because more compact in search engine (would otherwise write "True")
    human = 0 
    nature = 0 
    animal = 0 

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

    if pur in animal_category_list:
        animal = 1
    
    return human, nature, animal


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
        fieldnames = ["OfficialID", "Name", "City", "State", "Country", "Website", "HUM", "NAT", "ANI", "SourceURL", "SourceDate"]
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
                city, state = get_values_from_address(line["Principal Office/Trustees Address"])
                human, nature, animal = get_category_values(line["Purposes"])
                output_writer.writerow({"OfficialID": line["Charity Number"], 
                                        "Name": line["Charity Name"], 
                                        "City": city,
                                        "State": state, 
                                        "Country": "SC", 
                                        "Website": line["Website"], 
                                        "HUM": human, 
                                        "NAT": nature, 
                                        "ANI": animal, 
                                        "SourceURL": source_url, 
                                        "SourceDate": source_date})

    # print first couple of lines as check
    with open(output_file_path) as lines:
        print(colored("First two lines of created file:", 'green') )
        print(lines.readline(), end='')
        print(lines.readline(), end='')

    print(colored("Ended cleaning CSV file", "green")) 

