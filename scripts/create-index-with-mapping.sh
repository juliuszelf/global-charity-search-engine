
# We create index before uploading, so we have field of right type, like Country as a Keyword.

# Create the index
curl -X PUT "localhost:9200/chars"

echo "Index created"

# Update both mappings

# categories:
# HUM = human, .. will use as 'other' perhaps.
# NAT = nature, 
# ANI = animal, 
# EDU = education, 
# HEA = health, 
# COM = community, 
# REL = religion, 
# CUL = culture, 
# SPO = sports, 

curl -X PUT "localhost:9200/chars/_mapping?pretty" -H 'Content-Type: application/json' -d'
{
  "properties": {
    "Name": {
      "type": "text"
    },
    "City": {
      "type": "text"
    },
    "State": {
      "type": "keyword"
    },
    "Country": {
      "type": "keyword"
    },
    "Website": {
      "type": "keyword"
    },
    "HUM": {
      "type": "keyword"
    },
    "NAT": {
      "type": "keyword"
    },
    "ANI": {
      "type": "keyword"
    },
    "EDU": {
      "type": "keyword"
    },
    "HEA": {
      "type": "keyword"
    },
    "COM": {
      "type": "keyword"
    },
    "REL": {
      "type": "keyword"
    },
    "CUL": {
      "type": "keyword"
    },
    "SPO": {
      "type": "keyword"
    },
    "SourceDate": {
      "type": "keyword"
    },
    "OfficialID": {
      "type": "keyword"
    }
  }
}
'

echo "Mapping for index created"
