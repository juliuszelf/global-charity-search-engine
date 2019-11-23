# SUBFOLDER_NAMES holds a list like: a b
# Assuming subfolders 'a' and 'b' are only existing folders in 'data' folder.
# SUBFOLDER_NAMES := $(shell cd data && ls -d */ | tr -d '/' | tr '\n' ' ') 

# Goal is to generate a list like this based on all available subfolders of data
# SUBFOLDERS := data/a/created.txt data/b/created.txt 
# SUBFOLDERS := $(SUBFOLDER_NAMES:%:data/%/created.txt)
# SUBFOLDERS := $(SUBFOLDER_NAMES:%:%.txt)

# find results in paths like: ./data/a/source.txt
# we use 'cut' to make into: data/a/source.txt
# BFOLDERS := $(shell find . -name source.txt | cut -c 3- | tr '\n' ' ')
TARGETS := $(shell find . -name source.txt | cut -c 3- | tr '\n' ' ' | sed 's/source.txt/created.txt/g')


all: $(TARGETS)

# Problem is I want the target to be created.txt not source.txt
data/%/created.txt: data/%/step1.txt
	cat $^ > $@ && echo "created for $@" >> $@;

data/%/step1.txt: data/%/step0.txt
	cat $^ > $@ 

data/%/step0.txt: data/%/source.txt
	cat $^ > $@
