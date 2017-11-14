'''
Created on Sep 17, 2017

@author: duncan
'''

from utils.DBUtils import dbConnection
from sqlite3 import IntegrityError
from mock.mock import self
import logging

logging.basicConfig(filename='/tmp/upwork.log', filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

class upwork_item:
    
    def __init__(self):
        self.job_description=""
        self.job_time_elapse=""
        self.job_payment=""
        self.job_type=""
        self.title=""
        self.keyword_id=""
        self.link=""

class dao:
    
    def save_item(self,upwork_item):
        other_info="Job type: %s, Job pay: %s" %(upwork_item.job_type,upwork_item.job_payment)
        dbUtil = dbConnection()
        cur = dbUtil.get_cursor()
        try:
            cur.execute("insert into jobs(detail,time_created,site_id,title,link,other_info,keyword_id) values(?,datetime('now'),2,?,?,?,?)" ,
                             (upwork_item.job_description,upwork_item.title,upwork_item.link,other_info,upwork_item.keyword_id) )
               
        except IntegrityError,e:
            logger.error(e, exc_info=True)
        
        finally:
            dbUtil.commit()
        
        