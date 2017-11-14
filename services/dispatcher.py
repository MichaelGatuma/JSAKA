'''
Created on Nov 14, 2017

@author: duncan
'''

import schedule
import time
from model.dao import Subscription
from model.dao import Job


class Mailer:
    
    def __init__(self):
        '''pass'''
        
    def sendMail(self,message,attachements=None):
        '''pass'''
        
    
class Colletor:
    
    def __init__(self):
        '''pass'''
        
    def collect(self):
        job_dao=Job()
        jobs=job_dao.get_raw_jobs()
        all_jobs=[]
        for job in jobs:
            if job[4]!=0:
                job_entity={}
                job_specifications={}
                job_specifications['detail']=job[1]
                job_specifications['time_created']=job[2]
                job_specifications['site_id']=job[3]
                job_specifications['status']=job[4]
                job_specifications['titile']=job[5]
                job_specifications['link']=job[6]
                job_specifications['other_info']=job[7]
                job_specifications['keyword_id']=job[8]
                job_entity[job[0]]=job_specifications
                all_jobs.append(job_entity)
                
        subscription_dao =Subscription()        
        suscriptions=subscription_dao.fetch_raw_subscriptions()
        for subsc in suscriptions:
            "select "

class Cleaner:
    '''Cleans up jobs that have been dispathed to all subscribers'''
    
    

if __name__== "__main__":
    collector = Colletor()
    schedule.every(20).minutes.do(collector.collect())

    while True:
        schedule.run_pending()
        time.sleep(1)
        
        
        
        
        