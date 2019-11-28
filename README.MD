# About the Project
A global charity search engine.

- All data from official open data sources.
- Scripts to fully automate processing source files.

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

- Install python libraries using `requirements.txt`. You can install globally with `python3.6 -m pip install -r requirements.txt`.
- `make`. It will download source files and process to .json file, and split it into parts that are uploadable to ES.
- `docker-compose up -d` to start Elastic Search (ES), Kibana (interface to play with ES) and Flask.
- Once ES is fully started, assuming it's still empty, do `bash scripts/upload.sh` to upload file(s) to elastic search. 

# Usage

## Play around with search

Go to `http://localhost:5601` for Kibana interface where you can search using the console. 

More info on how to do search queries in the Kibana console: 

https://www.elastic.co/guide/en/kibana/7.4/console-kibana.html 

## Search page

Go to `http://localhost:5000` for the website where the search bar can be used once built.

# Roadmap

## 1.0 A working search engine

- Scripts to automate getting sourcefile and converting it to .json ready to upload to ES. [DONE]
- Dataset for single country (Canada), with minimal data [DONE]:
    - Name, City, Country, Website, sourceURL, sourceDate.
- Flask serving a page with working search bar. [TODO]

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

