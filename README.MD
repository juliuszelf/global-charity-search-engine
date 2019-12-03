# About the Project
A global charity search engine.

- All data from official open data sources.
- Scripts to fully automate processing source files.

Test it out at: http://charitysearch.juliuszelf.nl

Background info on the concept at: http://juliushuijnk.nl/project/charitius/

## Built With

- Scripts to process source files (Python3, Bash, Make)
- Docker
- Flask 
- Elastic Search

# Getting Started
## Prerequisites

- Docker installed
- Python 3.6 installed

## Installation

### Install Python libraries

The scripts that manipulate the CSV files, use python libraries.

- You can install the required python libraries globally with `python3.6 -m pip install -r requirements.txt`.

### Create data to search

- Type `make` in the root folder. It will download source files, process to .json file, and split it into parts that are uploadable to ES.

### Create docker-compose.override.yml file

#### During development

During development we want to make use of a Kibana container, but in production we don't want to make that available, since it costs RAM memory to run, but is not used. Therefore the production docker-compose file is different from production (live) version.

- We extend the `docker-compose.yml` file with the `docker-compose.override.yml`. During development let the override yml file hold the content of `docker-compose.dev.yml` by creating a symlink: `ln -s docker-compose.dev.yml docker-compose.override.yml`

#### For production (live)

- Make symlink connecting the prod file: `ln -s docker-compose.prod.yml docker-compose.override.yml`

### Start containers

- Type `docker-compose up -d`, it will take a minute or two for Elastic Search to fully start.
- Veriry container are running with `docker ps`, it should show `es01` and `flask`. During development also `kib01`.

### Upload charity data

- Once ES is fully started, assuming it's still empty, do `bash scripts/upload.sh` to upload file(s) to elastic search. 
- Verify the expected number of records ('documents') using: `curl -X GET "localhost:9200/_cat/count/chars?pretty"`
- Verify the expected structure of data using: `curl -X GET "localhost:9200/chars/?pretty"`

# Usage

## Play around with search 

Go to `http://localhost:5601` for Kibana interface where you can search using the console. 

More info on how to do search queries in the Kibana console: 

https://www.elastic.co/guide/en/kibana/7.4/console-kibana.html 

## Search page

For development the website is available via `http://localhost:5000`, it contains the search bar.

For production (live) the website is on port 80 (default port).

# Replace data & update code

On live server you might need to re-upload the data to ES, since the mapping of the fields has changed. In this case you can:

- Remove all data with: `curl -X DELETE "localhost:9200/chars?pretty"`
- You might als need to recreate all json file with: `rm data/*/*json*`
- (And perhaps remove even more files)
- Use `make` to create new json files to upload if required.
- Upload to ES via `bash scripts/upload-all.sh`

After you did a `git pull` or otherwise updated the Flask code, 
you might need to do `docker restart flask01` in order to let the changes go into effect.

# Roadmap

## 1.0 A working search engine [ DONE ]

Most basic working search engine.
- Name, City, Country, Website, sourceURL, sourceDate.

## Beyond 1.0

Iterate:
- Datasets from more countries.
- Improved scripts to upload to ES replacing old files.
- Improved ways to search, for instance with categories.

I use the [todo.taskpaper](todo.taskpaper) file to keep track of my TODO's. 

You may read the `todo.taskpaper` file, but it's probably (partly) in Dutch and could be outdated. This README.md file should make sense and be up te date.
 
# Contributing

If you'd like to help, great! You can do so by:

- Suggesting code or feature improvements.
- Suggest good open data sources.

There is no fixed process yet. If you have suggestions, leave an issue over here, or contact me directly.

# License

Distributed under the GNU GPLv3 license.  In short: Use it freely, share improvements with me, no warranties.

See [LICENSE.md](LICENSE.md) for more information.

Easy to comprehend page on license:

https://choosealicense.com/licenses/gpl-3.0/

# Contact

Julius Huijnk | [@Juliu on Twitter](https://www.twitter.com/juliu) | http://www.juliushuijnk.nl

