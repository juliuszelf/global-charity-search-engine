
# list all subfolders of data/ like "canada new-zealand"
COUNTRIES := $(shell cd data && ls -d */ | tr -d '/' | tr '\n' ' ') 
# COUNTRIES  = $(shell ls -d data/*)
# COUNTRY_NAMES = $(COUNTRIES:data/%/=%)

# Convert to .json file ready to upload to ES
${COUNTRIES}: data/%/%.es.json: data/%/%.clean.csv 
	@echo "Convert to .json for country: "$@
	cd scripts && python3 ./toJson.py $@ chars && cd ../

# trick to trigger target when python script is called
${COUNTRIES}: data/%/%.es.json: scripts/toJson.py 
	touch $@

# Only take required columns
data/%/%.clean.csv: data/%/%.rawutf8.csv scripts/%/cleanCSV.py 
	@echo "Clean csv (take required columns) for country: "$@
	cd scripts/$@ && python3 ./cleanCSV.py && cd ../../

# Convert to utf8
data/%/%.rawutf8.csv: data/%/%.raw.csv scripts/%/toUTF8.sh 
	@echo "Convert to utf8 (if required) for country: "$@
	bash scripts/$@/toUTF8.sh data/$@/$@.raw.csv data/$@/$@.rawutf8.csv

# Download
data/%/%.raw.csv: data/%/source.txt
	@echo "Downloading source file for: "$@
	curl -K data/$@/source.txt -o data/$@/$@.raw.csv
	@echo "Downloading done for: "$@

