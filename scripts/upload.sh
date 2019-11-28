echo "Uploading file $1 parts to Elastic Search.."
for i in $1-part-*; 
do 
	# Only upload the parts, not the es.json itself
	# $i includes the 'data/<country>/', hence the *
	if [[ $i == *-part-* ]];
	then
        echo "Uploading file $i"

		# "head -c100" ensures we only see first 100 characters of result, making it easier to see what happens
		curl -r 0-199- -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/_bulk --data-binary "@$i" | head -c100
	fi
done

echo "Upload ended."
