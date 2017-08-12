'''
Created on Aug 7, 2017

@author: duncan
'''

from utils.DBUtils import dbConnection
import sqlite3 as lite



class Keywords():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def  fetchAllKeyWords(self):
        dbUtil = dbConnection()
        cur = dbUtil.getCursor() 
        cur.execute("select keyword_id,keyword from keyword")
        keyWordList = {}
        keywords = cur.fetchall()
        for keyword in keywords:
            keyWordList[keyword[0]] = keyword[1]
            dbUtil.closeDbConnection()
        return  keyWordList       
    
    def updateKeyword(self,keyword, keyword_id):
        dbUtil = dbConnection()
        cur = dbUtil.getCursor()
        try:
            cur.execute("update keyword set keyword=? where keyword_id=?", (keyword, keyword_id)) 
            dbUtil.commit()
        except lite.IntegrityError:
            return  ("Keyword already exists", 501)
        return  "Keyword Updated Successfully"
    
    def deleteKeyword(self,keyword_id):
        dbUtil = dbConnection()
        cur = dbUtil.getCursor()
        cur.execute("delete from keyword where keyword_id=?", (keyword_id) )
        dbUtil.commit()
        return  "Keyword Deleted Successfully"
    
    def addKeyword(self,keyword):
        dbUtil = dbConnection()
        cur = dbUtil.getCursor()
        try:
            cur.execute("insert into keyword(keyword) values(?)", (keyword)) 
            dbUtil.commit()
        except lite.IntegrityError:
            return  ("Keyword already exists", 501)
        return  "Keyword created Successfully"    
    
class Subscription():
    def __init__(self):
        '''
        Constructor
        '''
        
    def addSubscription(self,subscription):
        sqlIsertUserMail="insert into subscriber(email) values(?)"
        sqlFetchEmailId="select subscriber_id from subscriber where email=?"
        sqlInsertSubscription='''insert into site_keyword(subscriber_id,site_id,keyword_id) 
        values(?,?,?)
        '''
        dbUtil = dbConnection()
        cur = dbUtil.getCursor()
        email=(subscription.getMail(),)
        print(subscription.getMail())
        print(email[0])
        try:
            try:
                cur.execute(sqlIsertUserMail,email) 
            except lite.IntegrityError:
                return("Email already exists", 501)
            dbUtil.commit()
            cur.execute(sqlFetchEmailId,(email[0],)) 
            mailId = cur.fetchone()
            print("Mail id")
            print(mailId)
            s=subscription.getSite()
            s=str(s).replace('\"', '\'')
            s=str(s).replace('[', '')
            s=str(s).replace(']', '')
            s=str(s).replace('\'', '')
            print(s)
            for site in s:
                print(site)
                v=subscription.getKeywords()
                v=str(v).replace('\"', '\'')
                v=str(v).replace('[', '')
                v=str(v).replace(']', '')
                v=str(v).replace('\'', '')
                for keyword in v.split(','):
                    cur.execute(sqlInsertSubscription,(mailId[0],site,keyword)) 
                    dbUtil.commit()
            return  ("Subscription added successfully")
        except lite.IntegrityError:
            return  ("Unable to save subscription", 501)
        
        ''' 
            Fetches all Subscribers in the database and returns a dictionary of Subscibers
        '''
        
    def fetchAllSubscribers(self):
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
        
    
    def deleteSubscription(self,subscriber_id):
        try:
            dbUtil = dbConnection()
            cur = dbUtil.getCursor()
            cur.execute("delete from subscriber where subscriber_id=?", (subscriber_id,)) 
            cur.execute("delete from site_keyword where subscriber_id=?", (subscriber_id,)) 
            dbUtil.commit()
        except lite.IntegrityError:
            return ("Failed to delete subscription", 501)
        return  "Keyword Deleted Successfully"
 
        
    