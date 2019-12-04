#!/usr/bin/env python3
from xlsx2csv import Xlsx2csv
import sys
import csv
import json
from termcolor import colored
import os

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

# first rename (copy) to a .xlsx so the convertion library understands this
# resumes script called from root
xlsx_file_path = "data/australia/australia_temp_raw.xlsx"
temp_file_path = "data/australia/australia_temp_raw.csv"
os.rename(input_file_path,xlsx_file_path)

Xlsx2csv(xlsx_file_path, outputencoding="utf-8").convert(temp_file_path)

# after the conversion the temp file will be the imputfile for creating json
input_file_path = temp_file_path

"""
TODO: inlezen csv als standard in stream
de csv filteren op relevante kolommen
toevoegen nieuwe kolommen
"""

source_url = "https://data.gov.au/dataset/ds-dga-b050b242-4487-4306-abf5-07ca073e5594/details?q=acnc"
source_date =  "01/12/2019"  # Better would be to dynamically get this 

# we assume it data has heading like this:
"""
ABN,CABN,Charity_Legal_Name,Other_Organisation_Names,Operating_Countries,Address_Type,Address_Line_1,Address_Line_2,Address_Line_3,Town_City,State,Postcode,Country,Charity_Website,Registration_Date,Date_Organisation_Established,Charity_Size,Number_of_Responsible_Persons,Financial_Year_End,Operates_in_ACT,Operates_in_NSW,Operates_in_NT,Operates_in_QLD,Operates_in_SA,Operates_in_TAS,Operates_in_VIC,Operates_in_WA,PBI,HPC,Preventing_or_relieving_suffering_of_animals,Advancing_Culture,Advancing_Education,Advancing_Health,Promote_or_oppose_a_change_to_law__government_poll_or_prac,Advancing_natual_environment,Promoting_or_protecting_human_rights,Purposes_beneficial_to_ther_general_public_and_other_analogous,Promoting_reconciliation__mutual_respect_and_tolerance,Advancing_Religion,Advancing_social_or_public_welfare,Advancing_security_or_safety_of_Australia_or_Australian_public,Another_purpose_beneficial_to_the_community,Aboriginal_or_TSI,Aged_Persons,Children,Communities_Overseas,Ethnic_Groups,Gay_Lesbian_Bisexual,General_Community_in_Australia,Men,Migrants_Refugees_or_Asylum_Seekers,Pre_Post_Release_Offenders,People_with_Chronic_Illness,People_with_Disabilities,People_at_risk_of_homelessness,Unemployed_Person,Veterans_or_their_families,Victims_of_crime,Victims_of_Disasters,Women,Youthharity_Legal_Name,Other_Organisation_Names,Operating_Countries,Address_Type,Address_Line_1,Address_Line_2,Address_Line_3,Town_City,State,Postcode,Country,Charity_Website,Registration_Date,Date_Organisation_Established,Charity_Size,Number_of_Responsible_Persons,Financial_Year_End,Operates_in_ACT,Operates_in_NSW,Operates_in_NT,Operates_in_QLD,Operates_in_SA,Operates_in_TAS,Operates_in_VIC,Operates_in_WA,PBI,HPC,Preventing_or_relieving_suffering_of_animals,Advancing_Culture,Advancing_Education,Advancing_Health,Promote_or_oppose_a_change_to_law__government_poll_or_prac,Advancing_natual_environment,Promoting_or_protecting_human_rights,Purposes_beneficial_to_ther_general_public_and_other_analogous,Promoting_reconciliation__mutual_respect_and_tolerance,Advancing_Religion,Advancing_social_or_public_welfare,Advancing_security_or_safety_of_Australia_or_Australian_public,Another_purpose_beneficial_to_the_community,Aboriginal_or_TSI,Aged_Persons,Children,Communities_Overseas,Ethnic_Groups,Gay_Lesbian_Bisexual,General_Community_in_Australia,Men,Migrants_Refugees_or_Asylum_Seekers,Pre_Post_Release_Offenders,People_with_Chronic_Illness,People_with_Disabilities,People_at_risk_of_homelessness,Unemployed_Person,Veterans_or_their_families,Victims_of_crime,Victims_of_Disasters,Women,Youth
"""
# For new file we are going to first rewrite the heading
# We keep: Legal Name, City, Country, Website
# We add: Source URL, Source date
end_part = source_url + "," + source_date + "\n" 

def fix_nulls(s):
    for line in s:
        yield line.replace('\0', ' ')

print("Opening output file..")
with open(output_file_path, 'w+', encoding="utf-8") as output_file:
     
    print("Write header..")
    fieldnames = ["Name", "City", "Country", "Website", "SourceURL", "SourceDate"]
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
            output_writer.writerow({"Name": line["Charity_Legal_Name"], 
                                    "City": line["Town_City"], 
                                    "Country": "AU", 
                                    "Website": line["Charity_Website"], 
                                    "SourceURL": source_url, 
                                    "SourceDate": source_date})

# print first couple of lines as check
with open(output_file_path) as lines:
  print(colored("First two lines of created file:", 'green') )
  print(lines.readline(), end='')
  print(lines.readline(), end='')

# Remove temp
print(colored("Removing temp file: " + xlsx_file_path, 'grey') )
os.remove(xlsx_file_path)
print(colored("Removed " + xlsx_file_path, 'yellow') )

print(colored("Removing temp file: " + temp_file_path 'grey') )
os.remove(temp_file_path)
print(colored("Removed " + temp_file_path 'yellow') )

print(colored("Ended cleaning CSV file", "green")) 

