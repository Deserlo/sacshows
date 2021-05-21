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

@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        result = request.form
        print(result)
        img_link = result['img_link']
        if result['venue'] == '':
            #create new venue and insert into Venues coll. 
            add_venue(result)
            v_link = result['venue url']
            v_name = result['venue text']
            if img_link == '':
                img_link = result['logo image']
        else:
            v = json.loads(result['venue'])
            v_link = v['link']
            v_name = v['venue']
            if img_link == '':
                img_link = v['logo image']
        new_show_post = {
            "venue calendar": v_link,
            "price": result['price'].lower(),
            "ages": result['ages'].lower(),
            "img link": img_link,
            "date": datetime.datetime.strptime(result['event_date'], '%Y-%m-%dT%H:%M'),
            "performers": result['performers'].lower(),
            "show": result['show'].lower(),
            "venue": v_name.lower(),
            "youtube id": "",
            "youtube snippet": "",
            "doors": result['doors'].lower(),
            "tickets link": result["tickets_link"],
            "uuid": shortuuid.uuid()[:11],
            "title": result['title'].lower(),
            "comments": result['comments'].lower()
        }  
        print(new_show_post) 
        mongo.db.Events.insert(new_show_post)
        return render_template("add_show_result.html", result=new_show_post)
    else:
        venue_names = mongo.db.Venues.find({})
        return render_template("add_show.html", venue_names=venue_names)

def add_venue(venue_info):
    new_venue_post = {
        'venue': venue_info['venue text'].lower(),
        'link': venue_info['venue url'],
        'logo image': venue_info['logo image'],
        'building image': venue_info['building image'],
        'instagram': venue_info['instagram'],
        'facebook': venue_info['facebook'],
        'city': venue_info['city'].lower(),
        'neighborhood': venue_info['neighborhood'].lower(),
        'address': venue_info['address'].lower(),
        'google map link': venue_info['google map link'],
        'phone': venue_info['phone'],
        'comments': venue_info['comments'].lower()
    }
    print(new_venue_post)
    mongo.db.Venues.insert(new_venue_post)


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



@app.route("/venue/<name>")
def venue_page(name):
    name = name.lower()
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=.5)
    query = { "venue": name, 'date': {'$gte': yesterday}  }
    venue_info = mongo.db.Venues.find_one({"venue": name})
    venue_events = mongo.db.Events.find(query).sort('date', 1)
    num_results = venue_events.count()
    return render_template('venue(show copy).html', title=str(num_results), venue_info=venue_info, venue_events=venue_events)


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