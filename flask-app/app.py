# flask-app/app.py

from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import os

# For debugging with breakpoints it can be nice to run outside docker container.
# First the container must be stopped via `docker stop flask01`.
# The app.py can't use same Elastic Search (ES) address as from inside docker network.
# To signal starting app.py outside docker containers, you add 'outside' like this:
# `python3 app.py outside` 
import sys

firstarg = sys.argv[1]

app = Flask(__name__)

# get analytics id
try:
    analytics_id = os.environ['ANALYTICS']
    print("analytics set")
except:
    print("no analytics set")

if firstarg == "outside":
    es_client = Elasticsearch('http://0.0.0.0:9200')
    print("connecting ES from the 'outside' to 0.0.0:9200")
else:
    es_client = Elasticsearch('http://es01:9200')

# For now we track this by hand, 
# so filters don't try to filter on countries that are not categorized yet.
countries_with_categories = ["AU", "SC", "GB-NIR"]


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


@app.route("/", methods=["GET", "POST"])
def home():
    title = "Global charity search engine"
    message = ""
    print("on home()")
    try:
        values_dict = request.args.to_dict()
        search_value = values_dict['search']
        if not search_value:
            return render_template("main.html", title=title, message="Please fill in a search word")

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

        response = s.execute()

        nr_results_shown = response['hits']['total']['value']
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
                               title=title,
                               nr_results=nr_results_shown,
                               results=found_charities,
                               searched_for=search_value,
                               message=message,
                               countries=selected_countries,
                               categories=selected_categories,
                               analytics=analytics_id
                               )
    except KeyError:
        print("no search")

    return render_template("main.html", title=title, content="no search..")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
