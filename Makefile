
# list all subfolders of data/ like "canada new-zealand"
COUNTRIES := $(shell cd data && ls -d */ | tr -d '/' | tr '\n' ' ') 
# COUNTRIES  = $(shell ls -d data/*)
# COUNTRY_NAMES = $(COUNTRIES:data/%/=%)


all: ${COUNTRIES}

${COUNTRIES}: 
	@echo "COUNTRY:"$@

# Convert to .json file ready to upload to ES
data/canada/canada.es.json: data/canada/canada.clean.csv scripts/toJson.py
	cd scripts && python3 ./toJson.py canada chars && cd ../

# Only take required columns
data/canada/canada.clean.csv: data/canada/canada.rawutf8.csv scripts/canada/cleanCSV.py
	cd scripts/canada && python3 ./cleanCSV.py && cd ../../

# Convert to utf8
data/canada/canada.rawutf8.csv: data/canada/canada.raw.csv scripts/canada/toUTF8.sh
	bash scripts/canada/toUTF8.sh data/canada/canada.raw.csv data/canada/canada.rawutf8.csv

# Download
data/canada/canada.raw.csv: data/canada/source.txt
	curl -K data/canada/source.txt -o data/canada/canada.raw.csv
