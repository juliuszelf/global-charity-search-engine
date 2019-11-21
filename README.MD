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
- Python3 installed
- Some python libraries installed like termcolors. Better documentation on this is a TODO.

## Installation

- `make`. It will download source files and process to .json file.
- `docker-compose up -d` to start Elastic Search (ES).
- Once ES is fully started, `bash scripts/upload.sh` to upload json file(s) to elastic search.


# Usage

Go to `http://localhost:5601` for Kibana interface where you can search using the console. 

More info on how to do search queries in the Kibana console: 

https://www.elastic.co/guide/en/kibana/7.4/console-kibana.html 

In future Flask served pages will provide a search bar.

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

