'''
Created on Jun 15, 2017

@author: duncan
'''
from flask import Flask, render_template
import sqlite3 as lite
from utils.DBUtils import dbConnection
from flask import request
from flask import jsonify
from meld.meldapp import app
from model.Dao import  Keywords

app = Flask(__name__)

@app.route('/index/')
def index():
    return render_template("index.html")

''' 
    Fetches all keywords in the database and retunrs a dictionary of keywords
'''


@app.route('/getAllKeywords/', methods=['GET'])
def getAllKeywords():
    keywords=Keywords()
    return jsonify(keywords.fetchAllKeyWords())
    


@app.route("/")
@app.route("/home/")
def home():
    keywords=Keywords()
    keyWordList = keywords.fetchAllKeyWords()    
    return  render_template('home.html', keyWordList=keyWordList)

@app.route('/edit-keyword/<keyword>/<keyword_id>/', methods=['PUT'])
def editKeyword(keyword=None, keyword_id=None):
    if keyword == None or id == None:
        return  ("No keyword selected", 501)  
    else:
        keywords=Keywords()
        return keywords.updateKeyword(keyword, keyword_id)
       
@app.route('/delete-keyword/<keyword_id>/', methods=['DELETE'])
def deleteKeyword(keyword_id=None):
    
    if keyword_id == None:
        return  ("No keyword specified", 501)
    else:
        keywords=Keywords()
        return keywords.deleteKeyword(keyword_id)
    
 
@app.route('/add-keyword/', methods=['POST'])
def addKeyword():
    print("Add keyword invoked")
    keyword = request.form['keyword']
    if keyword == None:
        print("No keyword")
        return  ("No keyword specified", 501)
    else:
        return  addKeyword(keyword)
    



# Site manage methods



''' 
    Fetches all Site in the database and returns a dictionary of keywords
'''

def fetchAllSites():
    print("Fetched sited----------> 1")
    dbUtil = dbConnection()
    cur = dbUtil.getCursor() 
    cur.execute("select site_id,name,alias from site")
    siteList = {}
    sites = cur.fetchall()
    for site in sites:
        if len(str(site[2]).strip())!=0 and site[2] is not None:          
            siteList[site[0]] = site[2]
        else:
            siteList[site[0]] = site[1]
    if(len(siteList)==0):
        siteList[0] = "There are no sites being scrapped"
    dbUtil.closeDbConnection()
    return  siteList       

@app.route('/getAllSites/', methods=['GET'])
def getAllSites():
    return jsonify(fetchAllSites())
    
@app.route('/getSiteKeywordMap/', methods=['GET'])
def getSiteKeywordMap():
    dbUtil = dbConnection()
    cur = dbUtil.getCursor() 
    cur.execute("select site_id,name,alias from site")
    siteKeywordMap = {}
    keywordList= []
    sites = cur.fetchall()

@app.route("/site/")
def site():
    nameList = fetchAllSites()    
    return  render_template('Site.html', nameList=nameList)

@app.route('/edit-name/<name>/<site_id>/', methods=['PUT'])
def editSite(name=None, site_id=None):
    if name == None or site_id == None:
        return  ("No keyword selected", 501)  
    else:
        dbUtil = dbConnection()
        cur = dbUtil.getCursor()
        try:
            cur.execute("update site set alias=? where site_id=?", (name, site_id)) 
            dbUtil.commit()
        except lite.IntegrityError:
            return  ("Name already exists", 501)
    return  "Name Updated Successfully"

        


# Subscription manage methods  ------------->>>>>


''' 
    Fetches all Subscribers in the database and returns a dictionary of Subscibers
'''

def fetchAllSubscribers():
    dbUtil = dbConnection()
    cur = dbUtil.getCursor() 
    
    subscriberDict = {}
    cur.execute("select * from subscriber")
    subscibers = cur.fetchall()
    cur.execute("select * from site_keyword")
    subscriptions = cur.fetchall()
    
    
    for subsc in subscibers: #Create a map of each subscriber and their subscription details(stats)
        subscriber={}
        subscriber['email'] = subsc[1]
        siteKeywordMap={}
        sitesId=[]
        uniqueSitesId=set()
        keyWordsId=[]
        for sub in subscriptions: #Get all sites and keywords subscriber is subscribed to
            if sub[0]==subsc[0]:
                sitesId.append(sub[1])
                uniqueSitesId.add(sub[1])
                keyWordsId.append(sub[2])
        for x in uniqueSitesId: # map keywords per site the subscriber is subscribed to
            kWords=[]
            for y in range(0,len(keyWordsId)):
                if sitesId[y]==x:
                    kWords.append(keyWordsId[y])
            siteKeywordMap[x]=kWords
                      
        subscriber['subs']= siteKeywordMap
        subscriber['totalSites']=len(uniqueSitesId)
        subscriber['totalKeywords']=len(keyWordsId)
        subscriberDict[subsc[0]]=subscriber
        
    dbUtil.closeDbConnection()
    return  subscriberDict       

@app.route('/getAllSubscribers/', methods=['GET'])
def getAllSubscribers():
    subscriberDict=fetchAllSubscribers()
    return jsonify(subscriberDict)
    
        


@app.route("/subscription/")
def getSubscription():
    return  render_template('subscriber.html', subscriptionList=fetchAllSubscribers())

@app.route('/edit-keyword/<keyword>/<keyword_id>/', methods=['PUT'])
def editSubscriber(keyword=None, keyword_id=None):
    if keyword == None or id == None:
        return  ("No keyword selected", 501)  
    else:
        print(keyword)
        dbUtil = dbConnection()
        cur = dbUtil.getCursor()
        try:
            cur.execute("update keyword set keyword=? where keyword_id=?", (keyword, keyword_id)) 
            dbUtil.commit()
        except lite.IntegrityError:
            return  ("Keyword already exists", 501)
    return  "Keyword Updated Successfully"

@app.route('/delete-keyword/<keyword_id>/', methods=['DELETE'])
def deleteSubscriber(keyword_id=None):
    if keyword_id == None:
        return  ("No keyword specified", 501)
    else:
        dbUtil = dbConnection()
        cur = dbUtil.getCursor()
        cur.execute("delete from keyword where keyword_id=?", (keyword_id,)) 
        dbUtil.commit()
    return  "Keyword Deleted Successfully"
 
@app.route('/add-subscriber/', methods=['POST'])
def addSubscriber():
    email=request.form['email']
    keywords = request.form['sites']
    keywords = request.form['keywords']
    
    return  "Keyword Deleted Successfully"
    






    
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8090)
    
