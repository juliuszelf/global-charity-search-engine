# flask-app/app.py

import json
from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

app = Flask(__name__)
es_client = Elasticsearch('http://es01:9200')

def set_category_human_filter(categories):
    # If no categories are checked, all should be true ("1")
    if "HUM" in categories or len(categories) == 0:
        return {"term" : { "HUM" : "1" }}
    else:
        return {"term" : { "HUM" : "0" }}



def set_category_nature_filter(categories):
    # If no categories are checked, all should be true ("1")
    if "NAT" in categories or len(categories) == 0:
        return {"terms" : { "NAT" : "1" }}
    else:
        return {"terms" : { "NAT" : "0" }}


def set_country_filters(countries):
    terms = []
    if not countries:
        # nothing checked, means no filter required
        countries = ["USA", "CA", "NZ", "AU", "GB-NIR", "SC"]

    for country in countries:
        terms.append({"term" : { "Country" : country }})
    return terms

@app.route("/", methods=["GET", "POST"])
def home():
    title = "Global charity search engine"
    print("on home()")
    try:
        values_dict = request.args.to_dict()
        search_value = values_dict['search']
        if not search_value:
            return render_template("main.html", title=title, content="Please fill in a search word")

        # for testing..
        content = ""
        
        # page_nr = values_dict['page']
        page_nr = 1
        countries = request.args.getlist('country')

        # For debugging
        cats = request.args.getlist('category')

        # TODO in function
        cat_hum = "0"
        cat_nat = "0"
        if "HUM" in cats:
            cat_hum = "1"
        if "NAST" in cats:
            cat_nat = "1"
        if len(cats) == 0:
            cat_hum = "1"
            cat_nat = "1"

        '''
        body = {
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": search_value,
                            "fields": [
                                "Name",
                                "City",
                            ]
                        }
                    },
                    "filter": {
                        "bool" : {
                            "should" : set_country_filters(countries),
                            "should" : set_category_human_filter(cats),
                            "should" : set_category_nature_filter(cats)
                            }
                    }
                }
            }
        }
        '''

        # TODO: Category should be of type field Facet or something in ES
        '''
        s = Search(using=es_client, index="chars") \
            .query("match", Name=search_value)   \
            .filter("terms", Country=countries) \
            .filter("term", HUM=cat_hum) \
            .filter("term", NAT=cat_nat) \
            '''

        s = Search(using=es_client, index="chars") \
            .query("match", Name=search_value)   \
            .filter("terms", Country=countries) \
            .filter("term", HUM=cat_hum) \
            .filter("term", NAT=cat_nat) \


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
                content=content,
                countries=countries,
                categories=cats,
                page_nr=page_nr)
    except KeyError:
        print("no search")

    return render_template("main.html", title=title, content="no search..")
    # return search_page


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

