# For australia we don't do UTF8 conversion here, 
# because it's actually a .xlsx file,
# We just make a copy so the makefile can be same for all data folders
RAW_CSV_FILE=$1
UTF_CSV_FILE=$2
cp $RAW_CSV_FILE $UTF_CSV_FILE
