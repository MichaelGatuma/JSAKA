'''
Created on Jun 15, 2017

@author: duncan
'''
from flask import Flask, render_template
from flask import jsonify
from flask import request

import json

from model.dao import Subscription
from model.dto import Subscription as subscriptioDto
from model.dao import Keyword
from model.dao import Site
from model.dto import Subscriber
from model.dao import Settings

app = Flask(__name__)

@app.route('/index/')
def index():
    return render_template("index.html")



# keyword manage endpoints

@app.route("/")
@app.route("/keyword/")
def keyword():
    keywords = Keyword()
    keyWordList = keywords.fetchAllKeyWords()    
    return  render_template('home.html', keyWordList=keyWordList)


''' 
    Fetches all keywords in the database and retunrs a dictionary of keywords
'''

@app.route('/getAllKeywords/', methods=['GET'])
def get_all_keywords():
    keywords = Keyword()
    return jsonify(keywords.fetchAllKeyWords())
    

@app.route('/edit-keyword/<keyword>/<keyword_id>/', methods=['PUT'])
def edit_keyword(keyword=None, keyword_id=None):
    if keyword == None or id == None:
        return  ("No keyword selected", 501)  
    else:
        keywords = Keyword()
        return keywords.updateKeyword(keyword, keyword_id)
       
       
@app.route('/delete-keyword/<keyword_id>/', methods=['DELETE'])
def delete_keyword(keyword_id=None):
    
    if keyword_id == None:
        return  ("No keyword specified", 501)
    else:
        keywords = Keyword()
        return keywords.deleteKeyword(keyword_id)
    
 
 
@app.route('/add-keyword/', methods=['POST'])
def add_keyword():
    keyword = request.form['keyword']
    if keyword == None:
        return  ("No keyword specified", 501)
    else:
        keywords = Keyword()
        return  keywords.addKeyword(keyword)
    



# Site manage endpoints

''' 
    Fetches all Site in the database and returns a dictionary of keywords
'''

@app.route('/getAllSites/', methods=['GET'])
def get_allSites():
    site = Site()
    return jsonify(site.fetchAllSites())
    

 

@app.route("/site/")
def site():
    site = Site()
    nameList = site.fetchAllSites()    
    return  render_template('Site.html', nameList=nameList)

@app.route('/edit-name/<name>/<site_id>/', methods=['PUT'])
def edit_site(name=None, site_id=None):
    if name == None or site_id == None:
        return  ("No keyword selected", 501)  
    else:
        site = Site() 
        return site.updateSite(name, site_id)
    



# Subscription manage endpoints  ------------->>>>>


@app.route('/getAllSubscribers/', methods=['GET'])
def get_allSubscribers():
    subDao = Subscription()
    subscriberDict = subDao.fetchAllSubscribers()
    return jsonify(subscriberDict)
    
        


@app.route("/subscription/")
def get_subscription():
    subDao = Subscription()
    return  render_template('subscriber.html', subscriptionList=subDao.fetchAllSubscriptions())

@app.route("/get_subscription_data/")
def get_subscriptions():
    subDao = Subscription()
    return  jsonify(subDao.fetchAllSubscriptions())

@app.route('/delete-subscription/<subscriber_id>/', methods=['DELETE'])
def delete_subscriber(subscriber_id=None):
    if subscriber_id == None:
        return  ("No Subscriber specified", 501)
    subDao = Subscription()
    returnVal = subDao.deleteSubscription(subscriber_id)
    return  returnVal
 
@app.route('/add-subscriber/', methods=['POST'])
def add_subscriber():
    email = request.form['email']
    keywords=json.loads(request.form['keywords'])
    sites=json.loads(request.form['sites'])
    
    for site in sites:
        subscriber = Subscriber(subscriber_id=None, subscriber_email=email)    
        subscription = subscriptioDto(site=sites, keyword=keywords, subscriber=subscriber)
    subDao = Subscription()
    returnVal = subDao.addSubscription(subscription)
    return  returnVal
    

@app.route('/update-subscriber/<subId>/', methods=['PUT'])
def update_subscriber(subId=None):
    if (subId == None):
        return("No subscriber selected selected", 501)  
    
    email = request.form['email']
    keywords=json.loads(request.form['keywords'])
    sites=json.loads(request.form['sites'])
    subscriber_group_id=subId.split("-")
    subscriber = Subscriber(subscriber_id=subscriber_group_id[0], subscriber_email=email)
    subscription = subscriptioDto(site=sites, keyword=keywords,subscription_group_id=subscriber_group_id[1],subscriber=subscriber)
    subDao = Subscription()
    returnVal = subDao.updateSubscription(subscription)
    return  returnVal
    
    
# Settings manage endpoints  ------------->>>>>    

@app.route("/get-settings/")
def fetch_all_settings():
    setting_dao = Settings()
    settings_list = setting_dao.fetchAllSettings()
    return jsonify(settings_list)
    

@app.route("/settings/")
def get_settings():
    return  render_template('settings.html')


# Jobs manage endpoints  ------------->>>>>    

@app.route("/jobs/")
def get_jobs():
    return  render_template('jobs.html')

 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)
    
