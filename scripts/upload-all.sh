# Must be called from root to work
# Assumption is that Elastic Search has no 'chars' index,
# and you want to create this now.

# First create index in ES
bash scripts/create-index-with-mapping.sh

echo "Going over each data folder"
for i in data/*/ 
do
	echo looking in folder $i

	# The upload script will look for the es.json-part-* files itself
	bash scripts/upload.sh "$i"es.json
done
