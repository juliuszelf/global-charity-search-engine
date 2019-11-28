# flask-app/app.py

import json
from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch('http://es01:9200')


search_page = """
    <form>
      <label for="site-search">Global charity search:</label>
      <input type="search" id="site-search" name="search" aria-label="Search charities">
      <button>Search</button>
    </form><br>
    <hr><br>
    """  

@app.route("/", methods=["GET", "POST"])
def home():
    try:
        search_value = request.args.to_dict()['search']
        res=es.search(index='chars', body={'query':{ 'match': {'Name': search_value}}})
        nr_results_shown = res['hits']['total']['value']
        results = res['hits']['hits']
        results_text = ""
        for result in results:
            result_content = result['_source']
            result_name = result_content['Name']
            result_city = result_content['City']
            result_country = result_content['Country']
            result_website = result_content['Website']
            result_text = "<b>" + result_name + "</b><br />"
            result_text += result_city + "," + result_country + "<br />"
            result_text += result_website + "<br />"

            results_text += result_text + "<hr><br>"

        return search_page \
                + "searched for: " + search_value + "<br><br>" \
                + "nr results: " + str(nr_results_shown) + "<br><br>" \
                + "<br><hr><br>" + str(results_text)
    except KeyError:
        print("no search")

    return search_page


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

