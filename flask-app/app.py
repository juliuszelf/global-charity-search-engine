# flask-app/app.py

from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import os
import logging

# For debugging with breakpoints it can be nice to run outside docker container.
# First the container must be stopped via `docker stop flask01`.
# The app.py can't use same Elastic Search (ES) address as from inside docker network.
# To signal starting app.py outside docker containers, you add 'outside' like this:
# `python3 app.py outside` 
import sys

firstarg = ""
try:
    firstarg = sys.argv[1]
except:
    print("no arguments passed to app.py")

app = Flask(__name__)

app.logger.setLevel(logging.INFO)

# get analytics id
try:
    analytics_id = os.environ['ANALYTICS']
    app.logger.info('analytics set')
except:
    analytics_id = ""
    app.logger.info('analytics not set')

if firstarg == "outside":
    es_client = Elasticsearch('http://0.0.0.0:9200')
    print("connecting ES from the 'outside' to 0.0.0:9200")
else:
    es_client = Elasticsearch('http://es01:9200')

# For now we track this by hand, 
# so filters don't try to filter on countries that are not categorized yet.
countries_with_categories = ["AU", "SC", "GB-NIR"]

# Elastic search has max results
max_results = 10000
results_per_page = 100


def set_category_values(cats):
    cat_hum = "0"
    cat_nat = "0"
    if "HUM" in cats:
        cat_hum = "1"
    if "NAT" in cats:
        cat_nat = "1"

    if len(cats) == 0:
        # No categories provided
        cat_hum = "1"
        cat_nat = "1"
    return cat_hum, cat_nat


def set_use_categories(selected_categories, selected_countries, countries_with_categories, message):
    # Decide use of category filters

    use = False
    also_non_categorized_countries = False
    categorized_in_selected = []

    if len(selected_categories) > 0:

        if len(selected_countries) == 0:
            # Assume no country selected, means all. And at least one has category
            use = True

            # Assuming not all countries have been categorized
            message += "Showing only results for categorized countries (" + ", ".join(countries_with_categories) + ")."
        else:
            # Check if values match
            # (I think list comprehensions are ugly and hard to read, so I prefer for loop)
            for c in selected_countries:
                if c in countries_with_categories:
                    # user selected a country with categories
                    use = True
                    categorized_in_selected.append(c)
                else:
                    also_non_categorized_countries = True
            if not use:
                # We have countries, but none have categories
                message += "None of the selected countries has been categorized, so ignoring category filter."

        if use and also_non_categorized_countries:
            message += "Showing only results for categorized countries (" + ", ".join(categorized_in_selected) + ")."

    return use, message


def page_start_end(page, per_page=results_per_page):
    """
    Set pagination via

    s = s[10:20]
    # can be seen as {"from": 10, "size": 10}

    Here we set 'start' value and 'end' value, so in example the 10 and 20.
    """

    if page < 1:
        page = 1
    offset = (per_page * page) - per_page

    start = offset
    end = offset + per_page
    return start, end


def page_from_dict(values_dict):
    page = values_dict.get('page', 1)
    try:
        page = int(page)
    except ValueError:
        page = 1
    if page < 1:
        page = 1
    return page


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    print("on home()")
    try:
        values_dict = request.args.to_dict()
        search_value = values_dict['search']
        page = page_from_dict(values_dict)

        if not search_value:
            return render_template("main.html",
                                   message="Please fill in a search word",
                                   analytics=analytics_id
                                   )

        s = Search(using=es_client, index="chars") \
            .query("multi_match", query=search_value, fields=['Name', 'City'])

        selected_countries = request.args.getlist('country')
        selected_categories = request.args.getlist('category')

        use_categories, message = set_use_categories(selected_categories,
                                                     selected_countries,
                                                     countries_with_categories,
                                                     message)

        if use_categories:
            cat_hum, cat_nat = set_category_values(selected_categories)
            s = s.filter("term", HUM=cat_hum)
            s = s.filter("term", NAT=cat_nat)

        if len(selected_countries) > 0:
            s = s.filter("terms", Country=selected_countries)

        start, end = page_start_end(page=page)
        s = s[start:end]

        response = s.execute()

        nr_results = response['hits']['total']['value']
        if nr_results == max_results:
            nr_results = str(max_results) + "+"

        results = response['hits']['hits']
        results_text = ""

        found_charities = []
        for result in results:
            result_content = result['_source']
            result_official_id = result_content['OfficialID']
            result_name = result_content['Name']
            result_city = result_content['City']
            result_state = result_content['State']  # State / Province
            result_country = result_content['Country']
            result_website = result_content['Website']
            result_source_url = result_content['SourceURL']
            result_source_date = result_content['SourceDate']

            if result_country == "USA" and len(result_official_id) > 2:
                # Guidestar url requires we turn an ID like: "811996576"
                # into "81-1996576"
                result_official_id = result_official_id[0:2] + "-" + result_official_id[2:]

            found_charities.append({
                "official_id": result_official_id,
                "name": result_name,
                "city": result_city,
                "state": result_state,
                "country": result_country,
                "website": result_website,
                "source_url": result_source_url,
                "source_date": result_source_date
            })
        if len(results) == 0:
            message += "No charities found for <i>" + search_value + "</i>"

        return render_template("main.html",
                               page=page,
                               nr_results=nr_results,
                               results=found_charities,
                               results_per_page=results_per_page,
                               searched_for=search_value,
                               message=message,
                               countries=selected_countries,
                               categories=selected_categories,
                               analytics=analytics_id
                               )
    except KeyError:
        print("no search")

    return render_template("main.html", content="no search..", analytics=analytics_id)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
