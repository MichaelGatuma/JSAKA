'''
Created on Sep 17, 2017

@author: duncan
'''

from utils.DBUtils import dbConnection

class upwork_item:
    
    def __init__(self):
        self.job_description=""
        self.job_time_elapse=""
        self.job_payment=""
        self.job_type=""
        self.title=""

class dao:
    
    def save_item(self,upwork_item):
        other_info="Job type: %s, Job pay: %s" %(upwork_item.job_type,upwork_item.job_payment)
        
        print("insert into jobs(detail,time_created,site_id,title,other_info) values('%s',datetime('now'),2,'%s','%s')" 
                         %(upwork_item.job_description,upwork_item.title,other_info) )
        
        dbUtil = dbConnection()
        cur = dbUtil.getCursor()
        cur.execute("insert into jobs(detail,time_created,site_id,title,other_info) values(?,datetime('now'),2,?,?)" ,
                         (upwork_item.job_description,upwork_item.title,other_info) )
        dbUtil.commit()   
        
        