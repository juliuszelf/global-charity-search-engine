# flask-app/app.py

from flask import Flask
app = Flask(__name__)

'''
TODO: confirm connection is ok
from elasticsearch import Elasticsearch
es = Elasticsearch('http://es01:9200')
'''

@app.route("/")
def home():
    return """
    <form>
      <label for="site-search">Global charity search:</label>
      <input type="search" id="site-search" name="q" aria-label="Search charities">
      <button>Search</button>
    </form>
    """


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

