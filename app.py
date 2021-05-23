from flask import Flask, render_template, redirect, request, url_for, session
from pymongo import MongoClient
from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import dumps
import sys
import os
import datetime
from datetime import date, timedelta
from datetime import timezone
from dotenv import load_dotenv
load_dotenv()
import shortuuid
import json

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')


MONGO_URI = os.getenv("MONGO_URI")
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        return search_by_date()
    query = request.args.get("args", "")
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=.5)
    title = "All Upcoming Shows By Date"
    if query == "asc":
        all_events = mongo.db.Events.find({'date': {'$gte': yesterday}}).sort('date', 1)
        title = "Earliest Upcoming Shows"
    elif query == "desc":
        all_events = mongo.db.Events.find({'date': {'$gte': yesterday}}).sort('date', -1)
        title = "Latest Upcoming Shows"
    else:
        all_events = mongo.db.Events.find({'date': {'$gte': yesterday}}).sort('date', 1)
    return render_template('index.html', title=title, events=all_events)

@app.route("/venues")
def venues():
    all_venues = mongo.db.Venues.find({})
    return render_template("venues_list.html", venues=all_venues)
    

@app.route("/venue/<name>")
def venue_page(name):
    name = name.lower()
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=.5)
    query = { "venue": name, 'date': {'$gte': yesterday}  }
    venue_info = mongo.db.Venues.find_one({"venue": name})
    venue_events = mongo.db.Events.find(query).sort('date', 1)
    num_results = venue_events.count()
    return render_template('venue.html', title=str(num_results), venue_info=venue_info, venue_events=venue_events)


@app.route("/search")
def search_by_date():
    date_from = request.values.get("date-from")
    date_to = request.values.get("date-to")
    if date_from != "" and date_to != "":
        from_date = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        to_date = datetime.datetime.strptime(date_to, '%Y-%m-%d')
        to_date += timedelta(days=1)
        query_range = { "date": { '$gte': from_date, '$lte': to_date} }
        search_results = mongo.db.Events.find(query_range).sort('date', 1)
        num_results = search_results.count()
        return render_template("index.html", title=str(num_results) + " Shows from " + date_from + " to " + date_to, events=search_results)
    elif date_from != "" and date_to == "":
        from_date = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        query_range = { "date": { '$gte': from_date} }
        search_results = mongo.db.Events.find(query_range).sort('date', 1)
        num_results = search_results.count()
        return render_template("index.html", title=str(num_results) + " Shows from " + date_from, events=search_results)
    elif date_from == "" and date_to != "":
        date = datetime.datetime.strptime(date_to, '%Y-%m-%d')
        query = { "date": date }
        search_results = mongo.db.Events.find(query).sort('date', 1)
        num_results = search_results.count()
        return render_template("index.html", title=str(num_results) + " Shows on " + date_to, events=search_results)
    else:
        title = "Upcoming Shows By Date"
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=.5)
        all_events = mongo.db.Events.find({'date': {'$gte': yesterday}}).sort('date', 1)
        num_results = all_events.count()
        return render_template('index.html', title=str(num_results) + " " + title, events=all_events)


@app.route("/all-ages")
def all_ages_page():
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=.5)
    query = { "ages": "all ages", 'date': { '$gte': yesterday}}
    all_ages_events = mongo.db.Events.find(query).sort('date', 1)
    return render_template("index.html", title="All Ages Shows", events=all_ages_events)


@app.route("/all-free")
def all_free_page():
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=.5)
    query = { "price": "free", 'date': { '$gte': yesterday}}
    free_events = mongo.db.Events.find(query).sort('date', 1)
    return render_template("index.html", title="Free Shows", events=free_events)


@app.route("/shows/<event_id>")
def show_event_page(event_id):
    event = mongo.db.Events.find_one({"uuid": event_id})
    new_events = just_listed()
    return render_template("show.html", title="Live Music Event Details", event=event, new_events=new_events)


def just_listed(): 
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=.5)
    query = {'date': {"$gte": yesterday}}
    new_events = mongo.db.Events.find(query).sort('_id', -1).limit(20)
    return new_events


@app.route("/just-listed")
def get_newly_listed_events():
    new_stuff = just_listed()
    return render_template("index.html", title="Newly Listed Shows", events=new_stuff)



@app.route("/submit")
def submit_event():
    return render_template("submit.html", title="Submit a show to Sactown Lowdown listings")


@app.route("/sac-locals")
def all_locals():
    query = request.args.get("args", "")
    if query == "asc":
        all_videos = mongo.db.Videos.find().sort('artist', 1)
    elif query == "desc":
        all_videos = mongo.db.Videos.find().sort('artist', -1)
    else:
        all_videos = mongo.db.Videos.find().sort('artist', 1)
    return render_template("videos.html", title="Sacramento's Local Music Artists", videos=all_videos)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)