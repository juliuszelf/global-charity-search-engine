# flask-app/app.py

import json
from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch('http://es01:9200')

@app.route("/", methods=["GET", "POST"])
def home():
    title = "Global charity search engine"
    try:
        search_value = request.args.to_dict()['search']
        res=es.search(index='chars', body={'query':{ 'match': {'Name': search_value}}})
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

        # result1 = { "name": "charityX", "city": "cityX"}
        return render_template("main.html", title=title, nr_results=nr_results_shown, results=found_charities, searched_for=search_value)
    except KeyError:
        print("no search")

    return render_template("main.html", title=title)
    # return search_page


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

