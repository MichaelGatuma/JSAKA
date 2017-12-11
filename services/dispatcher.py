'''
Created on Nov 14, 2017

@author: duncan
'''

import schedule
import time
from model.dao import Subscription
from model.dao import Job
from utils.DBUtils import dbConnection



    
def sendMail(self,message,attachements=None):
    '''pass'''
        

        
def jobs_colletor():
    dbUtil = dbConnection()
    cur = dbUtil.get_cursor()
    jobs_to_dispatch='''select tt1.subscriber_id,tt1.keyword_id,kyword.keyword,tt1.site_id,syt.name,tt1.detail,subsc.email  from 
                        (select sab.minimum_alert as jobs_no,sab.subscriber_id,sab.site_id,sab.keyword_id,
                        jb.detail,jb.job_id from subscription as sab,jobs as jb) tt1
                        inner join
                        (select count(*) as jobs_no,jobo.keyword_id as keyword_id,jobo.site_id as site_id,jobo.job_id from jobs jobo 
                        inner join subscription subs on subs.site_id=jobo.site_id and subs.keyword_id=jobo.keyword_id
                        inner join subscriber subscrib on subscrib.subscriber_id=subs.subscriber_id  
                        group by subscrib.email,jobo.keyword_id,jobo.site_id) tt2 
                        on tt1.site_id=tt2.site_id  and tt1.keyword_id=tt2.keyword_id and tt1.job_id=tt2.job_id
                        inner join subscriber subsc on tt1.subscriber_id=subsc.subscriber_id
                        inner join site syt on tt1.site_id=syt.site_id
                        inner join keyword kyword on tt1.keyword_id=kyword.keyword_id
                        where tt1.jobs_no<=tt2.jobs_no 
                        group by tt1.subscriber_id,tt1.keyword_id,tt1.site_id,tt1.job_id'''
    cur.execute(jobs_to_dispatch) 
    data_to_dispatch = cur.fetchall()
    if(data_to_dispatch!=None or len(data_to_dispatch)!=0):
                
            
def Cleaner:
    '''Cleans up jobs that have been dispathed to all subscribers'''
    
    

if __name__== "__main__":
    schedule.every(20).minutes.do(jobs_colletor())

    while True:
        schedule.run_pending()
        time.sleep(1)
        
        
        
        
        