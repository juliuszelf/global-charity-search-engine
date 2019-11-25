# Country specific script to turn raw file into utf-8 encoding
RAW_CSV_FILE=$1
UTF_CSV_FILE=$2
iconv -f ISO-8859-1 -t UTF-8  $RAW_CSV_FILE  > $UTF_CSV_FILE
