# flask-app/app.py

import json
from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch('http://es01:9200')

def set_category_human_filter(category_human):
    return {"terms" : { "HUM" : category_human }}

def set_category_nature_filter(category_human):
    return {"terms" : { "NAT" : category_human }}


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

        category_human = request.args.getlist('HUM')
        category_nature = request.args.getlist('NAT')

        # If both are not checked, then both are '1' (True) to be ok.
        if category_human == "0" and category_nature == "0":
            category_nature = "1"
            category_human = "1"

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
                            "should" : set_category_human_filter(category_human),
                            "should" : set_category_nature_filter(category_nature)
                            }
                    }
                }
            }
        }
        #{'query':{ 'match': {'Name': search_value}}}
        # res=es.search(index='chars', body={'query':{ 'match': {'Name': search_value}}})
        res=es.search(index='chars', body=body)
        nr_results_shown = res['hits']['total']['value']
        results = res['hits']['hits']
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
                page_nr=page_nr)
    except KeyError:
        print("no search")

    return render_template("main.html", title=title, content="no search..")
    # return search_page


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

