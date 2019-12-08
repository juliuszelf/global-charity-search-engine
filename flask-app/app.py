# flask-app/app.py

import json
from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

app = Flask(__name__)
es_client = Elasticsearch('http://es01:9200')

def set_category_values(cats):
    cat_hum = "0"
    cat_nat = "0"
    if "HUM" in cats:
        cat_hum = "1"
    if "NAST" in cats:
        cat_nat = "1"

    if len(cats) == 0:
        # No categories provided
        cat_hum = "1"
        cat_nat = "1"
    return cat_hum, cat_nat

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
        
        countries = request.args.getlist('country')


        cats = request.args.getlist('category')

        cat_hum, cat_nat = set_category_values(cats)

        # For now only Australia has categories
        if "AU" in countries:
            if len(countries) > 1:
                message = "Only Australia is categorized for now."

            # Not super scalable, but working solution
            # For dealing with 'no checkbox set means all are ok'.
            if len(countries) == 0:
                s = Search(using=es_client, index="chars") \
                    .query("multi_match", query=search_value, fields=['Name', 'City'])   \
                    .filter("term", HUM=cat_hum) \
                    .filter("term", NAT=cat_nat)
            else:
                s = Search(using=es_client, index="chars") \
                    .query("multi_match", query=search_value, fields=['Name', 'City'])   \
                    .filter("terms", Country=countries) \
                    .filter("term", HUM=cat_hum) \
                    .filter("term", NAT=cat_nat)
        else:
            # Don't filter on categories, because it will show no results otherwise
            if len(cats) > 0:
                # User has selected categories
                message = "Only Australia is categorized for now, so ignoring category filter."

            # Not super scalable, but working solution
            # For dealing with 'no checkbox set means all are ok'.
            if len(countries) == 0:
                s = Search(using=es_client, index="chars") \
                    .query("multi_match", query=search_value, fields=['Name', 'City'])
            else:
                s = Search(using=es_client, index="chars") \
                    .query("multi_match", query=search_value, fields=['Name', 'City'])   \
                    .filter("terms", Country=countries)

        #s.aggs.bucket('per_tag', 'terms', field='tags') \
        #    .metric('max_lines', 'max', field='lines')

        response = s.execute()

        #{'query':{ 'match': {'Name': search_value}}}
        # res=es.search(index='chars', body={'query':{ 'match': {'Name': search_value}}})
        # res=es_client.search(index='chars', body=body)
        nr_results_shown = response['hits']['total']['value']
        results = response['hits']['hits']
        results_text = ""

        found_charities = []
        for result in results:
            result_content = result['_source']
            result_name = result_content['Name']
            result_city = result_content['City']
            result_state = result_content['State'] # State / Province
            result_country = result_content['Country']
            result_website = result_content['Website']
         
            found_charities.append({ 
                "name": result_name, 
                "city": result_city,
                "state": result_state,
                "country": result_country,
                "website": result_website 
            })

        return render_template("main.html", 
                title=title, 
                nr_results=nr_results_shown, 
                results=found_charities, 
                searched_for=search_value, 
                message=message,
                countries=countries,
                categories=cats
                )
    except KeyError:
        print("no search")

    return render_template("main.html", title=title, content="no search..")
    # return search_page


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

