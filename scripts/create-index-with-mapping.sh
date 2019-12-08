
# We create index before uploading, so we have field of right type, like Country as a Keyword.

# Create the index
curl -X PUT "localhost:9200/chars"

echo "Index created"

# Update both mappings
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
    "SourceDate": {
      "type": "keyword"
    }
  }
}
'

echo "Mapping for index created"
