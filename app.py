'''
Created on Jun 15, 2017

@author: duncan
'''
from flask import Flask, render_template
from flask import jsonify
from flask import request

import json

from model.dao import Subscription
from model.dto import Subscription as subscriptio_dto
from model.dao import Keyword
from model.dao import Site
from model.dto import Subscriber
from model.dao import Settings
from meld.meldapp import app

app = Flask(__name__)

@app.route('/index/')
def index():
    return render_template("index.html")



# keyword manage endpoints

@app.route("/")
@app.route("/keyword/")
def keyword():
    keywords = Keyword()
    key_word_list = keywords.fetch_all_key_words()    
    return  render_template('home.html', key_word_list=key_word_list)


''' 
    Fetches all keywords in the database and retunrs a dictionary of keywords
'''

@app.route('/getAllKeywords/', methods=['GET'])
def get_all_keywords():
    keywords = Keyword()
    return jsonify(keywords.fetch_all_key_words())
    

@app.route('/edit-keyword/<keyword>/<keyword_id>/', methods=['PUT'])
def edit_keyword(keyword=None, keyword_id=None):
    if keyword == None or id == None:
        return  ("No keyword selected", 501)  
    else:
        keywords = Keyword()
        return keywords.update_keyword(keyword, keyword_id)
       
       
@app.route('/delete-keyword/<keyword_id>/', methods=['DELETE'])
def delete_keyword(keyword_id=None):
    
    if keyword_id == None:
        return  ("No keyword specified", 501)
    else:
        keywords = Keyword()
        return keywords.delete_keyword(keyword_id)
    
 
 
@app.route('/add-keyword/', methods=['POST'])
def add_keyword():
    keyword = request.form['keyword']
    if keyword == None:
        return  ("No keyword specified", 501)
    else:
        keywords = Keyword()
        return  keywords.add_keyword(keyword)
    



# Site manage endpoints

''' 
    Fetches all Site in the database and returns a dictionary of keywords
'''

@app.route('/getAllSites/', methods=['GET'])
def get_allSites():
    site = Site()
    return jsonify(site.fetch_all_sites())
    

 

@app.route("/site/")
def site():
    site = Site()
    name_list = site.fetch_all_sites()    
    return  render_template('Site.html', name_list=name_list)

@app.route('/edit-name/<name>/<site_id>/', methods=['PUT'])
def edit_site(name=None, site_id=None):
    if name == None or site_id == None:
        return  ("No keyword selected", 501)  
    else:
        site = Site() 
        return site.update_site(name, site_id)
    



# Subscription manage endpoints  ------------->>>>>


@app.route('/getAllSubscribers/', methods=['GET'])
def get_allSubscribers():
    sub_dao = Subscription()
    subscriberDict = sub_dao.fetch_all_subscribers()
    return jsonify(subscriberDict)
    
        


@app.route("/subscription/")
def get_subscription():
    sub_dao = Subscription()
    return  render_template('subscriber.html', subscriptionList=sub_dao.fetch_all_subscriptions())

@app.route("/get_subscription_data/")
def get_subscriptions():
    subDao = Subscription()
    return  jsonify(subDao.fetch_all_subscriptions())

@app.route('/delete-subscription/<subscriber_id>/', methods=['DELETE'])
def delete_subscriber(subscriber_id=None):
    if subscriber_id == None:
        return  ("No Subscriber specified", 501)
    sub_dao = Subscription()
    returnVal = sub_dao.delete_subscription(subscriber_id)
    return  returnVal
 
@app.route('/add-subscriber/', methods=['POST'])
def add_subscriber():
    email = request.form['email']
    keywords=json.loads(request.form['keywords'])
    sites=json.loads(request.form['sites'])
    
    for site in sites:
        subscriber = Subscriber(subscriber_id=None, subscriber_email=email)    
        subscription = subscriptio_dto(site=sites, keyword=keywords, subscriber=subscriber)
    sub_dao = Subscription()
    returnVal = sub_dao.add_subscription(subscription)
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
    subscription = subscriptio_dto(site=sites, keyword=keywords,subscription_group_id=subscriber_group_id[1],subscriber=subscriber)
    sub_dao = Subscription()
    returnVal = sub_dao.update_subscription(subscription)
    return  returnVal
    
    
# Settings manage endpoints  ------------->>>>>    

@app.route("/get-settings/")
def fetch_all_settings():
    setting_dao = Settings()
    settings_list = setting_dao.fetch_all_settings()
    return jsonify(settings_list)
    

@app.route("/settings/")
def get_settings():
    return  render_template('settings.html')


@app.route("/update-setting/", methods=['PUT'])
def update_setting():
    subscriber = request.form['subscriberId']
    keyword=request.form['keywordId']
    site=request.form['siteId']
    page_limit=request.form['pageLimit']
    minimum_alert=request.form['minimumAlert']
    subscription=subscriptio_dto(site,keyword,subscriber=subscriber,page_limit=page_limit,minimum_alert=minimum_alert)
    setting_dao = Settings()
    return jsonify(setting_dao.update_setting(subscription))
    
    
# Jobs manage endpoints  ------------->>>>>    

@app.route("/jobs/")
def get_jobs():
    return  render_template('jobs.html')

 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)
    
