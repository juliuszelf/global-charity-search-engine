TARGETS := $(shell find . -name source.txt | cut -c 3- | tr '\n' ' ' | sed 's/source.txt/es.json/g')
# Target holds list like: data/canada/es.json data/new-zealand/es.json

# SECONDARY will ensure the source files are not removed after creation.
# While developing this makes sense, but perhaps later beter to remove.
.SECONDARY: 

all: $(TARGETS)

# Convert to .json file ready to upload to ES
# (Adding script prerequisite for scripts/toJson.py breaks it, so leaving out for now)
data/%/es.json : data/%/clean.csv 
	@echo "Convert to .json for country: "$@
	# The $* should become the % of the target file, for instance 'canada'
	python3 scripts/toJson.py $* chars 

# Only take required columns
# (Adding script prerequisite for scripts/%/cleanCSV.py breaks it, so leaving out for now)
data/%/clean.csv: data/%/rawutf8.csv 
	@echo "Clean csv (take required columns) for country: "$@
	# For 'canada' turn into: python3 scripts/canada/cleanCSV.py data/canada/rawutf8.csv data/canada/clean.csv
	python3 scripts/$*/cleanCSV.py $^ $@ 

# Convert to utf8
# (Adding script prerequisite for scripts/%/toUTF8.sh breaks it, so leaving out for now)
data/%/rawutf8.csv: data/%/raw.csv 
	@echo "Convert to utf8 (if required) for country: "$@
	# For 'canada' turns into: bash scripts/canada/toUTF8.sh data/canada/raw.csv data/canada/rawutf8.csv
	bash scripts/$*/toUTF8.sh $^ $@

# Download
data/%/raw.csv: data/%/source.txt
	@echo "Downloading source file for: "$@
	curl -K $^ -o $@
	@echo "Downloading done for: "$@

