echo "Uploading file $1 to Elastic Search.."
curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/_bulk --data-binary "@$1";echo 

echo "Upload ended."
