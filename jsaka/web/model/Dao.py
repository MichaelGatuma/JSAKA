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
    def __init__(self, params):
        '''
        Constructor
        '''
        
    def addSubscription(self,subscription):
        sqlQuery="insert into "
        
        
        
        
    