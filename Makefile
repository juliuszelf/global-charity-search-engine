data/canada/canada.es.json: data/canada/canada.clean.csv scripts/toJson.py
	cd scripts && python3 ./toJson.py canada chars && cd ../

data/canada/canada.clean.csv: data/canada/canada.rawutf8.csv scripts/canada/cleanCSV.py
	cd scripts/canada && python3 ./cleanCSV.py && cd ../../

data/canada/canada.rawutf8.csv: data/canada/canada.raw.csv
	iconv -f ISO-8859-1 -t UTF-8  data/canada/canada.raw.csv > data/canada/canada.rawutf8.csv

data/canada/canada.raw.csv:
	curl https://www.canada.ca/content/dam/cra-arc/migration/cra-arc/gncy/stts/opendata/charity/2016/ident.csv -o data/canada/canada.raw.csv
