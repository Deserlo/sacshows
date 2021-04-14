from flask import Flask, render_template, redirect, request, url_for, session
from pymongo import MongoClient
from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import sys
import os
import datetime
from datetime import timezone
from dotenv import load_dotenv
load_dotenv()

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
    yesterday = today - datetime.timedelta(days=1.5)
    title = "Upcoming Shows By Date In Sacramento, Ca"
    if query == "asc":
        all_events = mongo.db.Events.find({'date': {'$gte': yesterday}}).sort('date', 1)
        title = "Earliest Upcoming Shows In Sacramento, Ca"
    elif query == "desc":
        all_events = mongo.db.Events.find({'date': {'$gte': yesterday}}).sort('date', -1)
        title = "Latest Upcoming Shows In Sacramento, Ca"
    else:
        all_events = mongo.db.Events.find({'date': {'$gte': yesterday}}).sort('date', 1)
    return render_template('index.html', title=title, events=all_events)



@app.route("/search")
def search_by_date():
    date_from = request.values.get("date-from")
    date_to = request.values.get("date-to")
    if date_from != "" and date_to != "":
        from_date = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        to_date = datetime.datetime.strptime(date_to, '%Y-%m-%d') 
        query_range = { "date": { '$gte': from_date, '$lte': to_date} }
        search_results = mongo.db.Events.find(query_range).sort('date', 1)
        num_results = search_results.count()
        return render_template("index.html", title=str(num_results) + " Shows from " + date_from + " to " + date_to + " In Sacramento, Ca", events=search_results)
    elif date_from != "" and date_to == "":
        from_date = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        query_range = { "date": { '$gte': from_date} }
        search_results = mongo.db.Events.find(query_range).sort('date', 1)
        num_results = search_results.count()
        return render_template("index.html", title=str(num_results) + " Shows from " + date_from +  " In Sacramento, Ca", events=search_results)
    elif date_from == "" and date_to != "":
        date = datetime.datetime.strptime(date_to, '%Y-%m-%d')
        query = { "date": date }
        search_results = mongo.db.Events.find(query).sort('date', 1)
        num_results = search_results.count()
        return render_template("index.html", title=str(num_results) + " Shows on " + date_to +  " In Sacramento, Ca", events=search_results)
    else:
        title = "Upcoming Shows By Date In Sacramento, Ca"
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1.5)
        all_events = mongo.db.Events.find({'date': {'$gte': yesterday}}).sort('date', 1)
        num_results = all_events.count()
        return render_template('index.html', title=str(num_results) + " " + title, events=all_events)


@app.route("/all-ages")
def all_ages_page():
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1.5)
    query = { "ages": "all ages", 'date': { '$gte': yesterday}}
    all_ages_events = mongo.db.Events.find(query).sort('date', 1)
    return render_template("index.html", title="All Ages Shows In Sacramento, Ca", events=all_ages_events)


@app.route("/all-free")
def all_free_page():
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1.5)
    query = { "price": "free", 'date': { '$gte': yesterday}}
    free_events = mongo.db.Events.find(query).sort('date', 1)
    return render_template("index.html", title="Free Shows In Sacramento, Ca", events=free_events)


@app.route("/shows/<event_id>")
def show_event_page(event_id):
    #evt = {"_id": {"$regex": ObjectId("604c3bf30000000000000000")}, "performers": event_id.split("-")[0]}
    #event = mongo.db.Events.find_one({"_id":{"$gte": ObjectId("604c3bf30000000000000000")}, "performers": event_id.split("-")[0].strip()})
    #query = {"$and": [{'_id': {"$gte": ObjectId("604c3bf30000000000000000")}}, {"venue": "b street theatre (live stream)"}]}
    event = mongo.db.Events.find_one({"uuid": event_id})
    new_events = just_listed()
    '''
    print("short id", event_id)
    eg from pp:
    query = {"$and": [{'_id': {"$gte": ObjectId("604c3bf30000000000000000")}}, "performers": event_id.split("-")[0].strip()]}
    ({_id:{$gte:ObjectId("604c3bf30000000000000000")}})
    #event = mongo.db.Events.find_one({"_id": ObjectId(event_id)})
    event = {"_id": {"$regex": ObjectId("604c3bf30000000000000000"))}}
    604c3bf30000000000000000
    604c3bf3cffde52b3eb8990e
    dt = event['_id'].generation_time
    timestamp = dt.replace(tzinfo=timezone.utc)
    dummy_id = ObjectId.from_datetime(timestamp)
    print("dummy id from utc:", dummy_id)
    evt = mongo.db.Events.find_one({"_id":{"$lt": dummy_id}, "performers": event['performers']})
    print("evt:", evt)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    print(timestamp)
    '''
    return render_template("show.html", title="Live Music Event Details", event=event, new_events=new_events)


def just_listed(): 
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1.5)
    #new_events = mongo.db.Events.find(sort=[( '_id', -1 ,{'date': {'$gte': yesterday}})]).limit(10)
    query = {'date': {"$gte": yesterday}}
    new_events = mongo.db.Events.find(query).sort('_id', -1).limit(10)
    '''
    print("short id", event_id)
    eg from pp:
    query = {"$and": [{'_id': {"$gte": ObjectId("604c3bf30000000000000000")}}, "performers": event_id.split("-")[0].strip()]}
    ({_id:{$gte:ObjectId("604c3bf30000000000000000")}})
    #event = mongo.db.Events.find_one({"_id": ObjectId(event_id)})
    event = {"_id": {"$regex": ObjectId("604c3bf30000000000000000"))}}
    604c3bf30000000000000000
    604c3bf3cffde52b3eb8990e
    dt = event['_id'].generation_time
    timestamp = dt.replace(tzinfo=timezone.utc)
    dummy_id = ObjectId.from_datetime(timestamp)
    print("dummy id from utc:", dummy_id)
    evt = mongo.db.Events.find_one({"_id":{"$lt": dummy_id}, "performers": event['performers']})
    print("evt:", evt)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    print(timestamp)
    '''
    return new_events



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
    #app.run()