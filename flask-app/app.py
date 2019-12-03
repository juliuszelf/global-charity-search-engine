# flask-app/app.py

import json
from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch('http://es01:9200')

def set_country_filters(countries):
    terms = []
    if not countries:
        # nothing checked, means no filter required
        countries = ["USA", "CA", "NZ"]

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
        # countries = values_dict['country']
        # countries = request.form.getlist('country')

        # for testing..
        content = "args: " + str(request.args.getlist('country'))
        
        # page_nr = values_dict['page']
        page_nr = 1
        countries = request.args.getlist('country')

        '''
        // If the country is set as field type 'keyword' (not text)
        // this query works.:
        GET chartest/_search
        {
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": "Monica",
                            "fields": [
                                "Name",
                                "City"
                            ]
                        }
                    },
                    "filter": {
                        "bool" : {
                        "should" : [
                            {"term" : { "Country" : "CA" } },
                            {"term" : { "Country" : "NZ" } }

                        ]
                    }
                    }
                }
            }
        }
        '''
        # We pass along what fields we want to check for
        '''
        body = {
            "query": {
                "multi_match": {
                    "query": search_value,
                    "fields": ["Name", "City", "Country", "Website"]
                }
            }
        }
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
                        "should" : set_country_filters(countries)
                    }
                    }
                }
            }
        }
        #{'query':{ 'match': {'Name': search_value}}}
        # res=es.search(index='chars', body={'query':{ 'match': {'Name': search_value}}})
        res=es.search(index='chartest', body=body)
        nr_results_shown = res['hits']['total']['value']
        results = res['hits']['hits']
        results_text = ""

        found_charities = []
        for result in results:
            result_content = result['_source']
            result_name = result_content['Name']
            result_city = result_content['City']
            result_country = result_content['Country']
            result_website = result_content['Website']
         
            found_charities.append({ 
                "name": result_name, 
                "city": result_city,
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
    # TODO remove when cache is needed
    app.config["CACHE_TYPE"] = "null"

    app.run(debug=True, host="0.0.0.0")

