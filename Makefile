TARGETS := $(shell find . -name source.txt | cut -c 3- | tr '\n' ' ' | sed 's/source.txt/es.json/g')
# Target holds list like: data/canada/es.json data/new-zealand/es.json

all: $(TARGETS)

# Convert to .json file ready to upload to ES
data/%/es.json : data/%/clean.csv 
	@echo "Convert to .json for country: "$@
	# The $* should become the % of the target file, for instance 'canada'
	python3 scripts/toJson.py $* chars 

# required, but can't make prerequisite directly
data/%/clean.csv: scripts/toJson.py 
	touch $@

# Only take required columns
data/%/clean.csv: data/%/rawutf8.csv 
	@echo "Clean csv (take required columns) for country: "$@
	# cd scripts/canada && python3 ./cleanCSV.py && cd ../../
	python3 scripts/$*/cleanCSV.py

# required, but can't make prerequisite directly
data/%/rawutf8.csv: scripts/%/cleanCSV.py
	touch $@

# Convert to utf8
data/%/rawutf8.csv: data/%/raw.csv 
	@echo "Convert to utf8 (if required) for country: "$@
	# Assuming 'canada' turns into: bash scripts/canada/toUTF8.sh data/canada/raw.csv data/canada/rawutf8.csv
	bash scripts/$*/toUTF8.sh $^ $@

# required, but can't make prerequisite directly
data/%/raw.csv: scripts/%/toUTF8.sh
	touch $@

# Download
data/%/raw.csv: data/%/source.txt
	@echo "Downloading source file for: "$@
	curl -K $^ -o $@
	@echo "Downloading done for: "$@

