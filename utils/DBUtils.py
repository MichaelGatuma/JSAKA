'''
Created on Jun 15, 2017

@author: duncan
'''
import os.path

import sqlite3 as lite


class dbConnection:
    def __init__(self):
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "JSaka.db")
        print("The db path---------->" + db_path)
        self.__con = lite.connect(db_path)
        self.__cur = self.__con.cursor()
        self.__cur.execute("create table IF NOT EXISTS  jobs(job_id INTEGER PRIMARY KEY ASC,name TEXT(100) UNIQUE ,time_created TEXT(100),site_id INTEGER,status INTEGER(1) DEFAULT 0)")
        self.__cur.execute('''
            create table IF NOT EXISTS subscription( subscriber_id INTEGER, 
            site_id INTEGER, keyword_id INTEGER, page_limit INTEGER NOT NULL DEFAULT 1, minimum_alert INTEGER NOT NULL DEFAULT 1,subscription_group_id INTEGER,
            PRIMARY KEY(subscriber_id,site_id,keyword_id) )
        ''')
        self.__cur.execute("create table IF NOT EXISTS  subscriber(subscriber_id INTEGER PRIMARY KEY ASC,email TEXT(100) UNIQUE)")
        self.__cur.execute("create table IF NOT EXISTS  keyword(keyword_id INTEGER PRIMARY KEY ASC,keyword TEXT(100) UNIQUE)")  
        self.__cur.execute("create table IF NOT EXISTS  site(site_id INTEGER PRIMARY KEY ASC,name TEXT(100) UNIQUE,alias TEXT(100))")  
        self.__cur.execute("delete from jobs where (julianday('now') - julianday(time_created)) >= 4")
        self.__con.commit()
     
    
    def getCursor(self):
        return self.__cur
    
    def closeDbConnection(self):
        self.__con.close()
        
    def commit(self):
        self.__con.commit()
    
    def rollback(self):
        self.__con.rollback()
