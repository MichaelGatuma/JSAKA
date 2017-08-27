'''
Created on Jun 15, 2017

@author: duncan
'''
from flask import Flask, render_template
from flask import request
from flask import jsonify
from model.dao import Keyword
from model.dao import Site
from model.dao import Subscription
from model.dto import Subscription as subscriptioDto

app = Flask(__name__)

@app.route('/index/')
def index():
    return render_template("index.html")



# keyword manage endpoints

@app.route("/")
@app.route("/keyword/")
def keyword():
    keywords=Keyword()
    keyWordList = keywords.fetchAllKeyWords()    
    return  render_template('home.html', keyWordList=keyWordList)


''' 
    Fetches all keywords in the database and retunrs a dictionary of keywords
'''

@app.route('/getAllKeywords/', methods=['GET'])
def getAllKeywords():
    keywords=Keyword()
    return jsonify(keywords.fetchAllKeyWords())
    

@app.route('/edit-keyword/<keyword>/<keyword_id>/', methods=['PUT'])
def editKeyword(keyword=None, keyword_id=None):
    if keyword == None or id == None:
        return  ("No keyword selected", 501)  
    else:
        keywords=Keyword()
        return keywords.updateKeyword(keyword, keyword_id)
       
       
@app.route('/delete-keyword/<keyword_id>/', methods=['DELETE'])
def deleteKeyword(keyword_id=None):
    
    if keyword_id == None:
        return  ("No keyword specified", 501)
    else:
        keywords=Keyword()
        return keywords.deleteKeyword(keyword_id)
    
 
 
@app.route('/add-keyword/', methods=['POST'])
def addKeyword():
    keyword = request.form['keyword']
    if keyword == None:
        return  ("No keyword specified", 501)
    else:
        keywords=Keyword()
        return  keywords.addKeyword(keyword)
    



# Site manage endpoints

''' 
    Fetches all Site in the database and returns a dictionary of keywords
'''

@app.route('/getAllSites/', methods=['GET'])
def getAllSites():
    site=Site()
    return jsonify(site.fetchAllSites())
    

 

@app.route("/site/")
def site():
    site=Site()
    nameList = site.fetchAllSites()    
    return  render_template('Site.html', nameList=nameList)

@app.route('/edit-name/<name>/<site_id>/', methods=['PUT'])
def editSite(name=None, site_id=None):
    if name == None or site_id == None:
        return  ("No keyword selected", 501)  
    else:
        site=Site() 
        return site.updateSite(name, site_id)
    



# Subscription manage endpoints  ------------->>>>>


@app.route('/getAllSubscribers/', methods=['GET'])
def getAllSubscribers():
    subDao=Subscription()
    subscriberDict=subDao.fetchAllSubscribers()
    return jsonify(subscriberDict)
    
        


@app.route("/subscription/")
def getSubscription():
    subDao=Subscription()
    return  render_template('subscriber.html', subscriptionList=subDao.fetchAllSubscribers())




@app.route('/delete-subscription/<subscriber_id>/', methods=['DELETE'])
def deleteSubscriber(subscriber_id=None):
    if subscriber_id == None:
        return  ("No Subscriber specified", 501)
    subDao=Subscription()
    returnVal=subDao.deleteSubscription(subscriber_id)
    return  returnVal
 
@app.route('/add-subscriber/', methods=['POST'])
def addSubscriber():
    email=request.form['email']
    sites = request.form['sites']
    keywords = request.form['keywords']
    subscription = subscriptioDto(email,sites,keywords,None)
    subDao=Subscription()
    returnVal=subDao.addSubscription(subscription)
    return  returnVal
    

@app.route('/update-subscriber/<subId>/', methods=['PUT'])
def updateSubscriber(subId=None):
    if (subId==None):
        return("No subscriber selected selected", 501)  
    email=request.form['email']
    sites = request.form['sites']
    keywords = request.form['keywords']
   
    subscription = subscriptioDto(email,sites,keywords,subId)
    subDao=Subscription()
    returnVal=subDao.updateSubscription(subscription)
    return  returnVal
    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)
    
