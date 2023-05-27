# ...
import flask
import os

app = flask.Flask(__name__)
# there may be required if there is a config.py
# app.config.from_object('index.config')
# DATABASE_FILENAME = INSTA485_ROOT/'var'/'insta485.sqlite3'
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")
app.config["PAGERANK_FILE"] = "pagerank.out"
app.config["STOPWORD_FILE"] = "stopwords.txt"

import index.api  # noqa: E402  pylint: disable=wrong-import-position
# Load inverted index, stopwords, and pagerank into memory

# inverted index segments here
index.api.load_index()
