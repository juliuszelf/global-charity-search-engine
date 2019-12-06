# For Scotland the 'download.file' is actually a zip file, so we first unzip

# In principle DOWNLOADED_FILE should be path to 'download.file'
DOWNLOADED_FILE=$1  
UNZIP_FOLDER=$1_folder  
# In principle UTF_CSV_FILE should be path to 'rawutf8.csv''
UTF_CSV_FILE=$2
RAW_CSV_FILE=$2.raw

unzip $RAW_FILE -d $UNZIP_FOLDER

# Copy the unzipped csv to current folder. Assumes a single csv file.
cp $UNZIP_FOLDER/*.csv $RAW_CSV_FILE

# Country specific script to turn raw file into utf-8 encoding
iconv -f ISO-8859-1 -t UTF-8  $RAW_CSV_FILE  > $UTF_CSV_FILE

# TODO: perhaps remove files used in between.
# But first keep them for debugging
