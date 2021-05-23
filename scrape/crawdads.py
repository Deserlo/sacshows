# Import required modules
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
import datetime
import calendar
import requests
import traceback
import time
import re
import shortuuid
from pymongo import MongoClient
from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import dumps
import sys
import os
import datetime
from datetime import timezone
from dotenv import load_dotenv
load_dotenv()
import shortuuid
import pprint
import json
import re


class Mongo(object):

    def __init__(self, mongo_uri):
        self.connection_string = mongo_uri
        self.client = MongoClient(self.connection_string).Sactown.Events
    

    def find(self):
        '''
        Finds all documents
        '''
        cursor = self.client.find({})
        list_cur = list(cursor)
        json_docs = dumps(list_cur)
        return list_cur


    def update_all(self):
        #db.articles.update({},{$set: {"published":true}},false,true)
        self.client.update_many({},{"$set": { "uuid": shortuuid.uuid() } }, False, array_filters=None)
    
    def update_one(self, oid, val):
        self.client.update_one({"_id": oid},{"$set": { "comments": val}})

    def insert(self, new_post):
        self.client.insert_one(new_post)




# Request the page
def download_html():
    url = 'https://plugin.eventscalendar.co/widget.html?pageId=pw2ve&compId=comp-j2kve9zj&viewerCompId=comp-j2kve9zj&siteRevision=795&viewMode=site&deviceType=mobile&locale=en&regionalLanguage=en&width=280&height=645&instance=8FoX-8wNl65rnHGhhW-03zKB6sH14K7N-grnlGiqo48.eyJpbnN0YW5jZUlkIjoiYzc2YjBlMDEtNzdiZC00Mzg5LTk5M2EtNWJiY2FhMmI5ODlkIiwiYXBwRGVmSWQiOiIxMzNiYjExZS1iM2RiLTdlM2ItNDliYy04YWExNmFmNzJjYWMiLCJzaWduRGF0ZSI6IjIwMjEtMDQtMjVUMjA6NTU6MDMuMjQ1WiIsInZlbmRvclByb2R1Y3RJZCI6InByZW1pdW0iLCJkZW1vTW9kZSI6ZmFsc2UsImFpZCI6IjQ4ZWU3NDYyLTdlMzQtNDU5OC05OWE5LWZlZDk3ZDNjZjg0NyIsInNpdGVPd25lcklkIjoiNjQ2ZDEzODQtNjMyZS00OWYxLWFkYTgtOWEyZTU4MGRkMDc3In0&commonConfig=%7B%22brand%22:%22wix%22,%22bsi%22:%22da3bd297-3583-4ddd-8732-4e6b16fdd2fe%7C1%22,%22BSI%22:%22da3bd297-3583-4ddd-8732-4e6b16fdd2fe%7C1%22%7D&vsi=2e493866-ea56-497d-a23f-9cb5b96e51de'

    options = webdriver.ChromeOptions() 
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options, executable_path='chromedriver.exe')

    driver.get(url)

    time.sleep(3)

    #print(driver.page_source)
    source = driver.page_source
    with open("powerhouse_source.html", "w") as f:
        f.write(source)
    driver.quit()


def load_chrome_driver(url, arg1, arg2, arg3):
    wait_cond = arg1
    html_attr = arg2
    html_atrr_name = arg3
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options, executable_path='chromedriver.exe')
    driver.get(url)
    delay = 7 # seconds
    try:
        WebDriverWait(driver, delay).until(wait_cond((html_attr, html_atrr_name)))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")
        driver.close()
    time.sleep(5)
    return driver


crawdad_url = 'https://www.eventbrite.com/o/crawdads-on-the-river-19840875685'
ghod_url = "https://www.eventbrite.com/o/knowbody-25365730835"


def eventbrite_links(filename, url):
    arg1 = EC.presence_of_element_located
    arg2 = By.CLASS_NAME
    arg3 = 'eds-l-pad-hor-2'	
    driver = load_chrome_driver(url, arg1, arg2, arg3)
    soup = BeautifulSoup(driver.page_source, features="lxml")
    links = soup.find_all('a', class_='eds-event-card-content__action-link')
    links = list(set(links))
    with open(filename, "w") as f:
        for l in links:
            f.write(l['href'] + "\n")
    print (links)
    return links


def eventbrite_page(filepath,venue_name,venue_url):
    with open(filepath) as fp:
        lines = fp.readlines()
    arg1 = EC.presence_of_element_located
    arg2 = By.CLASS_NAME
    arg3 = 'event-listing__body'
    for event_url in lines:	
        driver = load_chrome_driver(event_url, arg1, arg2, arg3)
        soup = BeautifulSoup(driver.page_source, features="lxml")
        event = soup.find('div', class_='event-listing__body')
        event.find('source')
        for el in event.find_all('source', attrs = {'srcset' : True}):
            print (el['srcset'])
        listingCard = soup.find('section', class_='listing-info')
        eventDetailsData = listingCard.find_all('div', class_='event-details__data')
        print ("--------------------------------------")
        if eventDetailsData[0].find('p', class_='text-stressed') is not None:
            headliner = eventDetailsData[0].find('p', class_='text-stressed').text.strip()
            ytKeyword = headliner
            performer_div = eventDetailsData[0].find('div', class_='g-cell')
            all_performers_span = performer_div.find_all('span')
            if len(all_performers_span) >1:
                performers = ""
                count = 0
                ytKeyword = all_performers_span[count].text.replace(",", "").strip() #gets the first name in list or performers to perform youtube search
                while count < len(all_performers_span):
                    performers += all_performers_span[count].text.replace(",", "").strip() + ","
                    count = count + 1
                headliner = performers[:-1]
            date_str = eventDetailsData[1].find_all('p', limit=2)
        else:
            #need to get meta content from listing-hero-title on event page
            headliner = event.find('h1', class_='listing-hero-title').text.strip()
            print(headliner)
            print(type(headliner))
            date_str = eventDetailsData[0].find_all('p', limit=2)
            ytKeyword = headliner
        date = datetime.datetime.strptime(date_str[0].text.strip(), '%a, %b %d, %Y, %I:%M %p PDT')
        text_body_span_element = event.find_all('span', class_='text-body-large')
        price = event.find('div', class_='js-display-price').text.strip()
        print(date, venue_name, venue_url, headliner.strip(), price, event_url)
        #evt_scrape = myEvent(date, venue_name, url, doors, start, headliner.strip(), ages, price, event_url, yt_link, yt_title)
        #update(current_list, evt_scrape)
        #venue_list.append(evt_scrape)
        driver.close()
        driver.quit()

    



def crawdad_page():
    event_url = "https://www.eventbrite.com/e/superbad-at-crawdads-on-the-river-tickets-147690914501?aff=ebdsoporgprofile"
    venue_name = "crawdad's on the river"
    venue_url = "#"
    arg1 = EC.presence_of_element_located
    arg2 = By.CLASS_NAME
    arg3 = 'event-listing__body'	
    driver = load_chrome_driver(event_url, arg1, arg2, arg3)
    soup = BeautifulSoup(driver.page_source, features="lxml")
    event = soup.find('div', class_='event-listing__body')
    event.find('source')
    for el in event.find_all('source', attrs = {'srcset' : True}):
        print (el['srcset'])
    listingCard = soup.find('section', class_='listing-info')
    eventDetailsData = listingCard.find_all('div', class_='event-details__data')
    print ("--------------------------------------")
    if eventDetailsData[0].find('p', class_='text-stressed') is not None:
        headliner = eventDetailsData[0].find('p', class_='text-stressed').text.strip()
        ytKeyword = headliner
        performer_div = eventDetailsData[0].find('div', class_='g-cell')
        all_performers_span = performer_div.find_all('span')
        if len(all_performers_span) >1:
            performers = ""
            count = 0
            ytKeyword = all_performers_span[count].text.replace(",", "").strip() #gets the first name in list or performers to perform youtube search
            while count < len(all_performers_span):
                performers += all_performers_span[count].text.replace(",", "").strip() + ","
                count = count + 1
            headliner = performers[:-1]
        date_str = eventDetailsData[1].find_all('p', limit=2)
    else:
        #need to get meta content from listing-hero-title on event page
        headliner = event.find('h1', class_='listing-hero-title').text.strip()
        print(headliner)
        print(type(headliner))
        date_str = eventDetailsData[0].find_all('p', limit=2)
        ytKeyword = headliner
    date = datetime.datetime.strptime(date_str[0].text.strip(), '%a, %b %d, %Y, %I:%M %p PDT')
    text_body_span_element = event.find_all('span', class_='text-body-large')
    price = event.find('div', class_='js-display-price').text.strip()
    print(date, venue_name, venue_url, headliner.strip(), price, event_url)
    #evt_scrape = myEvent(date, venue_name, url, doors, start, headliner.strip(), ages, price, event_url, yt_link, yt_title)
    #update(current_list, evt_scrape)
    #venue_list.append(evt_scrape)
    driver.close()
    driver.quit()


def read_source_html():
    #Folsom PH Pub
    venue = ''
    img_link = ''
    venue_calendar = ''
    f = open(".html", encoding="utf8")     
    soup = BeautifulSoup(f, features="lxml")
    event_list = soup.find_all('div', class_='event text-font')
    MongoDB = Mongo(MONGO_URI)
    for i in event_list:
        sh_uid = shortuuid.uuid()[:11]
        l = i.text.strip()
        lines = l.split('\n')
        without_empty_strings = [string.lower() for string in lines if string != ""]
        print(without_empty_strings)
        performers = without_empty_strings[0]
        show = without_empty_strings[2].split("-")[0]
        date = without_empty_strings[1]
        show_date = date + " " + show
        print(show_date)
        event_date = datetime.datetime.strptime(show_date, '%A, %B %d, %Y %I:%M%p')
        print(event_date)
        post = { "date": event_date,
        "venue": venue,
        "venue calendar": venue_calendar,
        "doors": "",
        "show": show,
        "img link": img_link,
        "performers": performers,
        "title": performers,
        "ages": "",
        "price": "",
        "tickets link": venue_calendar,
        "youtube link": "",
        "youtube snippet": "",
        "comments": "",
        "uuid": sh_uid
        }
        print(post)
        MongoDB.insert(post)
    f.close()


#crawdad_links(filename="shows.txt", url="https://www.eventbrite.com/o/knowbody-25365730835")

eventbrite_page(filepath="shows.txt",venue_name="greathouse of dance",venue_url="#")