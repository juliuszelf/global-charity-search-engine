# We can't upload json when it's too large, so we split
split -l 100000 $1 $1-part-

# outcome was filenames like: es-part-xa, we turn those into es-part-xa.json
for i in $1-part-*; do mv "$i" "$i.json"; done

