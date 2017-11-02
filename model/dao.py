'''
Created on Aug 7, 2017

@author: duncan
'''

import sqlite3 as lite
from utils.DBUtils import dbConnection


class Keyword():
    '''
    Keyword class
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
    
    def updateKeyword(self, keyword, keyword_id):
        dbUtil = dbConnection()
        cur = dbUtil.getCursor()
        try:
            cur.execute("update keyword set keyword=? where keyword_id=?", (keyword, keyword_id)) 
            dbUtil.commit()
        except lite.IntegrityError:
            return  ("Keyword already exists", 501)
        return  "Keyword Updated Successfully"
    
    def deleteKeyword(self, keyword_id):
        dbUtil = dbConnection()
        cur = dbUtil.getCursor()
        cur.execute("delete from keyword where keyword_id=?", (keyword_id))
        dbUtil.commit()
        return  "Keyword Deleted Successfully"
    
    def addKeyword(self, keyword):
        dbUtil = dbConnection()
        cur = dbUtil.getCursor()
        try:
            cur.execute("insert into keyword(keyword) values(?)", (keyword,)) 
            dbUtil.commit()
        except lite.IntegrityError:
            return  ("Keyword already exists", 501)
        return  "Keyword created Successfully"    
    
    
    
class Subscription():
    def __init__(self):
        '''
        Constructor
        '''
        
    def addSubscription(self, subscription):
        sqlIsertUserMail = "insert into subscriber(email) values(?)"
        sqlFetchEmailId = "select subscriber_id from subscriber where email=?"
        sqlIncrementGroupId="insert into group_id_sequence values(null)"
        sqlInsertSubscription = '''insert into subscription(subscriber_id,site_id,keyword_id,page_limit,minimum_alert,subscription_group_id) 
        values(?,?,?,1,1,?)
        '''

        dbUtil = dbConnection()
        cur = dbUtil.getCursor()
        email = subscription.subscriber.subscriber_email
        generated_group_id=None
        try:
            try:
                cur.execute(sqlIsertUserMail, (email,) )
            except Exception,e:
                print("Email already exists")
            cur.execute(sqlIncrementGroupId) 
            dbUtil.commit()
            generated_group_id=cur.lastrowid
            cur.execute(sqlFetchEmailId, (email,)) 
            mailId = cur.fetchone()
            s=None
            k=None
            for site in subscription.site:
                s=site
                for keyword in subscription.keyword:
                    k=keyword
                    cur.execute(sqlInsertSubscription, (mailId[0], site, keyword,generated_group_id)) 
            dbUtil.commit()
            return  ("Subscription saved successfully")
        except lite.IntegrityError:
            dbUtil.rollback()
            sqlFetchSite = "select name from site where site_id=?"
            cur.execute(sqlFetchSite, (s,)) 
            st = cur.fetchone()
            sqlFetchKeyword = "select keyword from keyword where keyword_id=?"
            cur.execute(sqlFetchKeyword, (k,)) 
            ky = cur.fetchone()
            return  ("The entry, site: %s - Keyword: %s, exists" %(st[0],ky[0]), 501)
        
        
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
        
        for subsc in subscibers:  # Create a map of each subscriber and their subscription details(stats)
            subscriber = {}
            subscriber['email'] = subsc[1]
            siteKeywordMap = {}
            sitesId = []
            uniqueSitesId = set()
            keyWordsId = []
            for sub in subscriptions:  # Get all sites and keywords subscriber is subscribed to  
                if sub[1] == subsc[0]:
                    sitesId.append(sub[1])
                    if(sub[1] != None and sub[1] != ""):
                        uniqueSitesId.add(sub[1])
                    if(sub[2] != None and sub[2] != ""):
                        keyWordsId.append(sub[2])
            for x in uniqueSitesId:  # map keywords per site the subscriber is subscribed to
                kWords = []
                for y in range(0, len(keyWordsId)):
                    if sitesId[y] == x:
                        kWords.append(keyWordsId[y])
                siteKeywordMap[x] = kWords
            subscriber['subs'] = siteKeywordMap
            subscriber['totalSites'] = len(uniqueSitesId)
            subscriber['totalKeywords'] = len(keyWordsId)
            subscriberDict[subsc[0]] = subscriber
        dbUtil.closeDbConnection()
        return  subscriberDict  
        
        
    def fetchAllSubscriptions(self):
        subscriptions_list=[]
        subscriber_map={}
        site_id_name={}
        subscriber_id_mail={}
        keyword_id_name={}
        dbUtil = dbConnection()
        cur = dbUtil.getCursor() 
        cur.execute('''select * from subscription s inner join keyword  k on k.keyword_id= s.keyword_id 
                       inner join site site on site.site_id=s.site_id 
                       inner join subscriber subsc on subsc.subscriber_id=s.subscriber_id''')
        subscriptions = cur.fetchall()
        for subsc in subscriptions:
            try:
                subscriber_group_map=subscriber_map[subsc[0]]
                try:
                    site_map=subscriber_group_map[subsc[5]]
                    try:
                        keyword_list=site_map[subsc[1]]
                        keyword_list.append(subsc[2])
                    except KeyError,e:
                        site_map[subsc[1]]=[]
                        keyword_list=site_map[subsc[1]]
                        keyword_list.append(subsc[2])
                except KeyError,e:
                    subscriber_group_map[subsc[5]]={}
                    site_map=subscriber_group_map[subsc[5]]
                    site_map[subsc[1]]=[]
                    keyword_list=site_map[subsc[1]]
                    keyword_list.append(subsc[2])
            except KeyError,e:
                subscriber_map[subsc[0]]={}
                subscriber_group_map=subscriber_map[subsc[0]]
                subscriber_group_map[subsc[5]]={}
                site_map=subscriber_group_map[subsc[5]]
                site_map[subsc[1]]=[]
                keyword_list=site_map[subsc[1]]
                keyword_list.append(subsc[2])
            
            site_id_name[subsc[8]]=subsc[9]
            keyword_id_name[subsc[6]]=subsc[7]
            subscriber_id_mail[subsc[14]]=subsc[15]
            
        subscriptions_list.append(subscriber_map)
        subscriptions_list.append(site_id_name)
        subscriptions_list.append(keyword_id_name)
        subscriptions_list.append(subscriber_id_mail)
        print(subscriptions_list)
        return subscriptions_list
        
        
    def deleteSubscription(self, subscriber_group_id,subscriber_id=None, group_id=None):
        
        if(subscriber_id==None or group_id==None):
            subscriber_groupid=subscriber_group_id.split("-")
            subscriber_id=subscriber_groupid[0]
            group_id=subscriber_groupid[1]
        try:
            dbUtil = dbConnection()
            cur = dbUtil.getCursor()
            cur.execute("delete from subscription where subscriber_id=? and subscription_group_id=?", (subscriber_id,group_id)) 
            dbUtil.commit()
        except lite.IntegrityError:
            dbUtil.rollback()
            return ("Failed to delete subscription", 501)
        return  "Keyword Deleted Successfully"
 
    
    
    def updateSubscription(self, subscription):        
        sql_select_subscription="Select * from subscription where subscriber_id=? and site_id=? and keyword_id=? and subscription_group_id is not ?"
        sqlFetchEmailId = "select subscriber_id from subscriber where email=?"
        
        email = subscription.subscriber.subscriber_email
        
        dbUtil = dbConnection()
        cur = dbUtil.getCursor()
        cur.execute(sqlFetchEmailId, (email,)) 
        mailId = cur.fetchone()
        for site in subscription.site:
            s=site
            for keyword in subscription.keyword:
                k=keyword
                cur.execute(sql_select_subscription, (mailId[0], site, keyword, subscription.subscription_group_id)) 
                subscript = cur.fetchone()
                print("Haha")
                print(subscript)
                if(subscript!=None):
                    sqlFetchSite = "select name from site where site_id=?"
                    cur.execute(sqlFetchSite, (s,)) 
                    st = cur.fetchone()
                    sqlFetchKeyword = "select keyword from keyword where keyword_id=?"
                    cur.execute(sqlFetchKeyword, (k,)) 
                    ky = cur.fetchone()
                    return  ("The entry, site: %s - Keyword: %s, exists" %(st[0],ky[0]), 501)
        self.deleteSubscription(subscriber_group_id=None,subscriber_id=subscription.subscriber.subscriber_id,group_id=subscription.subscription_group_id)    
        self.addSubscription(subscription)
        return "Subscription updated Successfully"
        
    
class Site():
    
    def __init__(self):
        '''
        Constructor
        '''
    
    def fetchAllSites(self):
        dbUtil = dbConnection()
        cur = dbUtil.getCursor() 
        cur.execute("select site_id,name,alias from site")
        siteList = {}
        sites = cur.fetchall()
        for site in sites:
            if len(str(site[2]).strip()) != 0 and site[2] is not None:          
                siteList[site[0]] = site[2]
            else:
                siteList[site[0]] = site[1]
        if(len(siteList) == 0):
            siteList[0] = "There are no sites being scrapped"
        dbUtil.closeDbConnection()
        return  siteList       
    
    
    def updateSite(self, newName=None, site_id=None):
        if newName == None or site_id == None:
            return  ("No keyword selected", 501)  
        else:
            dbUtil = dbConnection()
            cur = dbUtil.getCursor()
            try:
                cur.execute("update site set alias=? where site_id=?", (newName, site_id)) 
                dbUtil.commit()
            except lite.IntegrityError:
                return  ("Name already exists", 501)
        return  "Name Updated Successfully"

    
    
    
class Settings():
    
    
    def fetchAllSettings(self):
        dbUtil = dbConnection()
        cur = dbUtil.getCursor() 
        cur.execute('''select * from setting 
                        inner join site on setting.site_id=site.site_id 
                        inner join keyword on keyword.keyword_id=setting.keyword_id
                        inner join subscriber on setting.subscriber_id = subscriber.subscriber_id;''')
        setting_map = {}
        settings = cur.fetchall()
        for setting in settings:
            setting_map[setting[0]]=setting
        dbUtil.closeDbConnection()
        return  setting_map  
    
    
    
    
    
    
    
    
