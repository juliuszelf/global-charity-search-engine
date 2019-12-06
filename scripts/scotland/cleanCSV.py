#!/usr/bin/env python3

import sys
import csv
import json
from termcolor import colored

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

# First clean csv, we can then re-use the csvToJSON script for all datasets.
source_url = "https://www.oscr.org.uk/about-charities/search-the-register/charity-register-download"
source_date = "2019"  

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
            city, state = get_values_from_address(line["Principal Office/Trustees Address"])
            output_writer.writerow({"Name": line["Charity Name"], 
                                    "City": city,
                                    "State": state, 
                                    "Country": "SC", 
                                    "Website": line["Website"], 
                                    "SourceURL": source_url, 
                                    "SourceDate": source_date})

# print first couple of lines as check
with open(output_file_path) as lines:
  print(colored("First two lines of created file:", 'green') )
  print(lines.readline(), end='')
  print(lines.readline(), end='')

print(colored("Ended cleaning CSV file", "green")) 

