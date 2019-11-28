# TODO loop over all uploadable files & upload

# Must be called from root to work

echo "Going over each data folder"
for i in data/*/ 
do
	echo looking in folder $i

	# The upload script will look for the es.json-part-* files itself
	bash scripts/upload.sh "$i"es.json
done
