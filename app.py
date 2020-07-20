from flask import Flask, render_template, redirect, request, url_for, session
from flask import jsonify
from pymongo import MongoClient
from flask import Flask
from flask_pymongo import PyMongo
import sys
import os
import datetime
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')


MONGO_URI = os.getenv("MONGO_URI")
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

@app.route("/")
def index():
    query = request.args.get("args", "")
    if query == "asc":
        all_events = mongo.db.Events.find({'date': { '$gte': datetime.datetime.now()}}).sort('date', 1)
    elif query == "desc":
        all_events = mongo.db.Events.find({'date': { '$gte': datetime.datetime.now()}}).sort('date', -1)
    else:
        all_events = mongo.db.Events.find({'date': { '$gte': datetime.datetime.now()}}).sort('date', 1)
    return render_template('index.html', title='All shows in Sacramento, Ca', events=all_events)


@app.route("/search")
def search_by_date():
    date_str = request.values.get("date")
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    query = { "date": date }
    search_results = mongo.db.Events.find(query)
    print ("Number of results: ", search_results.count())
    return render_template("index.html", title="Shows result Sactown Lowdown", events=search_results)


@app.route("/all-ages")
def all_ages_page():
    query = { "ages": "all ages", 'date': { '$gte': datetime.datetime.now()}}
    all_ages_events = mongo.db.Events.find(query)
    return render_template("index.html", title="All ages shows in Sacramento, Ca", events=all_ages_events)


@app.route("/all-free")
def all_free_page():
    query = { "price": "free", 'date': { '$gte': datetime.datetime.now()}}
    free_events = mongo.db.Events.find(query)
    return render_template("index.html", title="All free shows in Sacramento, Ca", events=free_events)


@app.route("/sac-locals")
def all_locals():
    query = request.args.get("args", "")
    print (query)
    if query == "asc":
        all_videos = mongo.db.Videos.find().sort('artist', 1)
    elif query == "desc":
        all_videos = mongo.db.Videos.find().sort('artist', -1)
    else:
        all_videos = mongo.db.Videos.find()
    return render_template("videos.html", title="Sac Locals", videos=all_videos)



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run()