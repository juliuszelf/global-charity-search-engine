#!/usr/bin/env python3

import sys
import csv
import json
from termcolor import colored

# First clean csv, we can then re-use the csvToJSON script for all datasets.
source_url = "https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf"
source_date = "11-nov-2019"


def fix_nulls(s):
    for line in s:
        yield line.replace('\0', ' ')

def parse(input_file_path, output_file_path):
    # we assume it data has heading like this:
    """
    EIN,NAME,ICO,STREET,CITY,STATE,ZIP,GROUP,SUBSECTION,AFFILIATION,CLASSIFICATION,
    RULING,DEDUCTIBILITY,FOUNDATION,ACTIVITY,ORGANIZATION,STATUS,TAX_PERIOD,ASSET_CD,
    INCOME_CD,FILING_REQ_CD,PF_FILING_REQ_CD,ACCT_PD,ASSET_AMT,INCOME_AMT,REVENUE_AMT,
    NTEE_CD,SORT_NAME
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

            for line in input_reader:
                output_writer.writerow({"OfficialID": line["EIN"], 
                                        "Name": line["NAME"], 
                                        "City": line["CITY"], 
                                        "State": line["STATE"], 
                                        "Country": "USA", 
                                        "Website": "",  # Not part of the source
                                        "HUM": "",
                                        "NAT": "",
                                        "ANI": "",
                                        "SourceURL": source_url, 
                                        "SourceDate": source_date})

    # print first couple of lines as check
    with open(output_file_path) as lines:
        print(colored("First two lines of created file:", 'green') )
        print(lines.readline(), end='')
        print(lines.readline(), end='')

    print(colored("Ended cleaning CSV file", "green")) 

