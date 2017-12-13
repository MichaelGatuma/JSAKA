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

    def  fetch_all_key_words(self):
        dbUtil = dbConnection()
        cur = dbUtil.get_cursor() 
        cur.execute("select keyword_id,keyword from keyword")
        key_word_list = {}
        keywords = cur.fetchall()
        for keyword in keywords:
            key_word_list[keyword[0]] = keyword[1]
            dbUtil.close_db_connection()
        return  key_word_list       
    
    def update_keyword(self, keyword, keyword_id):
        dbUtil = dbConnection()
        cur = dbUtil.get_cursor()
        try:
            cur.execute("update keyword set keyword=? where keyword_id=?", (keyword, keyword_id)) 
            dbUtil.commit()
        except lite.IntegrityError:
            return  ("Keyword already exists", 501)
        return  "Keyword Updated Successfully"
    
    def delete_keyword(self, keyword_id):
        dbUtil = dbConnection()
        cur = dbUtil.get_cursor()
        cur.execute("delete from keyword where keyword_id=?", (keyword_id))
        dbUtil.commit()
        return  "Keyword Deleted Successfully"
    
    def add_keyword(self, keyword):
        dbUtil = dbConnection()
        cur = dbUtil.get_cursor()
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
        
    def add_subscription(self, subscription):
        sql_isert_user_mail = "insert into subscriber(email) values(?)"
        sql_fetch_email_id = "select subscriber_id from subscriber where email=?"
        sql_increment_group_id="insert into group_id_sequence values(null)"
        sql_insert_subscription = '''insert into subscription(subscriber_id,site_id,keyword_id,page_limit,minimum_alert,subscription_group_id) 
        values(?,?,?,1,1,?)
        '''

        dbUtil = dbConnection()
        cur = dbUtil.get_cursor()
        email = subscription.subscriber.subscriber_email
        generated_group_id=None
        try:
            try:
                cur.execute(sql_isert_user_mail, (email,) )
            except Exception,e:
                print("Email already exists")
            cur.execute(sql_increment_group_id) 
            dbUtil.commit()
            generated_group_id=cur.lastrowid
            cur.execute(sql_fetch_email_id, (email,)) 
            mailId = cur.fetchone()
            s=None
            k=None
            for site in subscription.site:
                s=site
                for keyword in subscription.keyword:
                    k=keyword
                    cur.execute(sql_insert_subscription, (mailId[0], site, keyword,generated_group_id)) 
            dbUtil.commit()
            return  ("Subscription saved successfully")
        except lite.IntegrityError:
            dbUtil.rollback()
            sql_fetch_site = "select name from site where site_id=?"
            cur.execute(sql_fetch_site, (s,)) 
            st = cur.fetchone()
            sqlFetchKeyword = "select keyword from keyword where keyword_id=?"
            cur.execute(sqlFetchKeyword, (k,)) 
            ky = cur.fetchone()
            return  ("The entry, site: %s - Keyword: %s, exists" %(st[0],ky[0]), 501)
        
        
    ''' 
    Fetches all Subscribers in the database and returns a dictionary of Subscibers
    '''
        
    def fetch_all_subscribers(self):
        dbUtil = dbConnection()
        cur = dbUtil.get_cursor() 
        
        subscriber_dict = {}
        cur.execute("select * from subscriber")
        subscibers = cur.fetchall()
        cur.execute("select * from site_keyword")
        subscriptions = cur.fetchall()
        
        for subsc in subscibers:  # Create a map of each subscriber and their subscription details(stats)
            subscriber = {}
            subscriber['email'] = subsc[1]
            siteKeywordMap = {}
            sitesId = []
            unique_sites_id = set()
            key_words_id = []
            for sub in subscriptions:  # Get all sites and keywords subscriber is subscribed to  
                if sub[1] == subsc[0]:
                    sitesId.append(sub[1])
                    if(sub[1] != None and sub[1] != ""):
                        unique_sites_id.add(sub[1])
                    if(sub[2] != None and sub[2] != ""):
                        key_words_id.append(sub[2])
            for x in unique_sites_id:  # map keywords per site the subscriber is subscribed to
                kWords = []
                for y in range(0, len(key_words_id)):
                    if sitesId[y] == x:
                        kWords.append(key_words_id[y])
                siteKeywordMap[x] = kWords
            subscriber['subs'] = siteKeywordMap
            subscriber['totalSites'] = len(unique_sites_id)
            subscriber['totalKeywords'] = len(key_words_id)
            subscriber_dict[subsc[0]] = subscriber
        dbUtil.close_db_connection()
        return  subscriber_dict  
    
    
    def fetch_raw_subscriptions(self):
        dbUtil = dbConnection()
        cur = dbUtil.get_cursor() 
        cur.execute('''select * from subscription s inner join keyword  k on k.keyword_id= s.keyword_id 
                       inner join site site on site.site_id=s.site_id 
                       inner join subscriber subsc on subsc.subscriber_id=s.subscriber_id''')
        subscriptions = cur.fetchall()
        return subscriptions
        
        
    def fetch_all_subscriptions(self):
        subscriptions_list=[]
        subscriber_map={}
        site_id_name={}
        subscriber_id_mail={}
        keyword_id_name={}
        dbUtil = dbConnection()
        cur = dbUtil.get_cursor() 
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
        
        
    def delete_subscription(self, subscriber_group_id,subscriber_id=None, group_id=None):
        
        if(subscriber_id==None or group_id==None):
            subscriber_groupid=subscriber_group_id.split("-")
            subscriber_id=subscriber_groupid[0]
            group_id=subscriber_groupid[1]
        try:
            dbUtil = dbConnection()
            cur = dbUtil.get_cursor()
            cur.execute("delete from subscription where subscriber_id=? and subscription_group_id=?", (subscriber_id,group_id)) 
            dbUtil.commit()
        except lite.IntegrityError:
            dbUtil.rollback()
            return ("Failed to delete subscription", 501)
        return  "Keyword Deleted Successfully"
 
    
    
    def update_subscription(self, subscription):        
        sql_select_subscription="Select * from subscription where subscriber_id=? and site_id=? and keyword_id=? and subscription_group_id is not ?"
        sql_fetch_email_id = "select subscriber_id from subscriber where email=?"
        
        email = subscription.subscriber.subscriber_email
        
        dbUtil = dbConnection()
        cur = dbUtil.get_cursor()
        cur.execute(sql_fetch_email_id, (email,)) 
        mailId = cur.fetchone()
        for site in subscription.site:
            s=site
            for keyword in subscription.keyword:
                k=keyword
                cur.execute(sql_select_subscription, (mailId[0], site, keyword, subscription.subscription_group_id)) 
                subscript = cur.fetchone()
                if(subscript!=None):
                    sqlFetchSite = "select name from site where site_id=?"
                    cur.execute(sqlFetchSite, (s,)) 
                    st = cur.fetchone()
                    sqlFetchKeyword = "select keyword from keyword where keyword_id=?"
                    cur.execute(sqlFetchKeyword, (k,)) 
                    ky = cur.fetchone()
                    return  ("The entry, site: %s - Keyword: %s, exists" %(st[0],ky[0]), 501)
        self.delete_subscription(subscriber_group_id=None,subscriber_id=subscription.subscriber.subscriber_id,group_id=subscription.subscription_group_id)    
        self.add_subscription(subscription)
        return "Subscription updated Successfully"
        
    
class Site():
    
    def __init__(self):
        '''
        Constructor
        '''
    
    def fetch_all_sites(self):
        dbUtil = dbConnection()
        cur = dbUtil.get_cursor() 
        cur.execute("select site_id,name,alias from site")
        site_list = {}
        sites = cur.fetchall()
        for site in sites:
            if len(str(site[2]).strip()) != 0 and site[2] is not None:          
                site_list[site[0]] = site[2]
            else:
                site_list[site[0]] = site[1]
        if(len(site_list) == 0):
            site_list[0] = "There are no sites being scrapped"
        dbUtil.close_db_connection()
        return  site_list       
    
    
    def update_site(self, new_name=None, site_id=None):
        if new_name == None or site_id == None:
            return  ("No keyword selected", 501)  
        else:
            dbUtil = dbConnection()
            cur = dbUtil.get_cursor()
            try:
                cur.execute("update site set alias=? where site_id=?", (new_name, site_id)) 
                dbUtil.commit()
            except lite.IntegrityError:
                return  ("Name already exists", 501)
        return  "Name Updated Successfully"

    
    
    
class Settings():
    
    
    def fetch_all_settings(self):
        dbUtil = dbConnection()
        cur = dbUtil.get_cursor() 
        cur.execute('''select * from subscription 
                        inner join site on subscription.site_id=site.site_id 
                        inner join keyword on keyword.keyword_id=subscription.keyword_id
                        inner join subscriber on subscription.subscriber_id = subscriber.subscriber_id;''')
        setting_list = []
        settings = cur.fetchall()
        for setting in settings:
            setting_list.append(setting)
        dbUtil.close_db_connection()
        return  setting_list  
    
    
    def update_setting(self,subscription):
        sql_setting="update subscription set page_limit=?,minimum_alert=? where subscriber_id=? and site_id=? and keyword_id=?"
        dbUtil = dbConnection()
        cur = dbUtil.get_cursor()
        try:
            cur.execute(sql_setting, (subscription.page_limit,subscription.minimum_alert,subscription.subscriber,subscription.site,subscription.keyword)) 
            dbUtil.commit()
        except Exception,e:
            return  ("Failed to update setting", 501)
        return  self.fetch_all_settings()
        
    
    
class Job:
    def __init__(self):
        '''pass'''
    
    
        
        