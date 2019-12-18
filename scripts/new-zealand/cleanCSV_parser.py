#!/usr/bin/env python3

import sys
import csv
import json
from termcolor import colored

# First clean csv, we can then re-use the csvToJSON script for all datasets.
source_url = "http://www.odata.charities.govt.nz/Organisations?$format=csv&$returnall=true&$filter=deregistrationdate%20eq%20null"
source_date = "2019"  # Not super sure about source date

def fix_nulls(s):
    for line in s:
        yield line.replace('\0', ' ')

def parse(input_file_path, output_file_path):
    # we assume it data has heading like this:
    """
    OrganisationId,AccountId,Name,CharityRegistrationNumber,WebSiteURL,
    EMailAddress1,Telephone1,Telephone2,TelephoneDay,Fax,
    PostalAddress_city,PostalAddress_country,
    PostalAddress_line1,PostalAddress_line2,PostalAddress_postcode,PostalAddress_suburb,
    StreetAddress_city,StreetAddress_country,StreetAddress_line1,StreetAddress_line2,
    StreetAddress_postcode,StreetAddress_suburb,CharityEmailAddress,
    CompaniesOfficeNumber,DateRegistered,deregistrationdate,
    Deregistrationreasons,EndOfYearDayofMonth,endofyearmonth,
    Establishedbyparliamentact,Excemptioncomment,Isincorporated,
    Maori_trust_brd,maoritrustapproved,Marae_funds,Marae_reservation,
    Notices,onlandunderTeTureWhenuaMaoriAct,Organisational_type,
    percentage_spent_overseas,RegistrationStatus,Society_institution,
    Trustees_trust,Exemptions,AnnualReturnDueDate,annualreturnextensiondate,
    GroupType,GroupId,MainActivityId,MainBeneficiaryId,MainSectorId,
    OtherNames,ModifiedOn,NZBNNumber
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
                output_writer.writerow({"OfficialID": line["NZBNNumber"], 
                                        "Name": line["Name"], 
                                        "City": line["StreetAddress_city"], 
                                        "State": "", 
                                        "Country": "NZ", 
                                        "Website": line["WebSiteURL"], 
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

