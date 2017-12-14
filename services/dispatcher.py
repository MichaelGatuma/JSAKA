'''
Created on Nov 14, 2017

@author: duncan
'''
import sys
sys.path.insert(0, "/home/duncan/workspace/JobsScapper")

import collections
import logging
import schedule
import time
from utils.DBUtils import dbConnection
from utils.mail import send_mail



        
def jobs_colletor():
    '''
        Collects jobs to be sent and packages then in a dictionary: jobs_proprties
        jobs_proprties: the key is the subscriber id, its value is a map of the jobs properties
        jobs_proprties value which is a map has its key in the format 'subscriber_id:site_id:keyword_id' ;
        the value is a list of the properties in the order: keyword_id, keyword,site_id, site_name,job_detail,email,job_link,post_time,other_info 
    '''
    dbUtil = dbConnection()
    cur = dbUtil.get_cursor()
    jobs_to_dispatch='''select tt1.subscriber_id as subscriber_id,tt1.keyword_id as keyword_id,
                    tt1.keyword as keyword,tt1.site_id as site_id,tt1.name as site_name,
                    jb.detail as job_detail,tt1.email as email,jb.link as job_link,
                    jb.time_created as post_time,jb.other_info as other_info,jb.job_id as job_id from 
                    (select subscrib.subscriber_id,subscrib.email,keyw.keyword_id,keyw.keyword,sit.site_id,sit.name,subscrip.minimum_alert as jobs_no,keyw.keyword,sit.name
                    from subscription subscrip 
                    inner join subscriber as subscrib on  subscrip.subscriber_id=subscrib.subscriber_id
                    inner join keyword keyw on subscrip.keyword_id=keyw.keyword_id
                    inner join site sit on subscrip.site_id=sit.site_id) as tt1,(select count(*) as jobs_no,jobo.keyword_id as keyword_id,jobo.site_id as site_id,subscrib.subscriber_id as subscriber_id from jobs jobo
                    inner join subscription subs on subs.site_id=jobo.site_id and subs.keyword_id=jobo.keyword_id
                    inner join subscriber subscrib on subscrib.subscriber_id=subs.subscriber_id  
                    group by subscrib.subscriber_id,jobo.keyword_id,jobo.site_id) as tt2
                    inner join jobs jb on 
                    tt1.site_id=jb.site_id  and tt1.keyword_id=jb.keyword_id and jb.job_id=jb.job_id
                    where  
                    tt1.site_id=tt2.site_id  and tt1.keyword_id=tt2.keyword_id and tt1.subscriber_id=tt2.subscriber_id and tt1.jobs_no<=tt2.jobs_no
                    and not exists (select 1 from sent_jobs where    tt1.subscriber_id=subscriber_id and jb.job_id=job_id)
                    order by tt1.subscriber_id,tt1.name,tt1.keyword
                    '''
    logger.info("Searching for pending jobs to send")
    cur.execute(jobs_to_dispatch) 
    data_to_dispatch = cur.fetchall()
    if(data_to_dispatch!=None or len(data_to_dispatch)!=0):
        jobs_proprties={}
        for job in data_to_dispatch:
            keyr=str(job[0])+':'+str(job[3])+':'+str(job[1])+':'+str(job[10])
            try:
                jobs_proprties[job[0]]
            except KeyError,e:
                logger.error(e)
                jobs_proprties[job[0]]=collections.OrderedDict()
           
            try:
                jobs_proprties[job[0]][keyr]
                jobs_proprties=_add_jobs_properties_to_list(jobs_proprties,job)
            except KeyError,e:
                logger.error(e)
                jobs_proprties[job[0]][keyr]=[]
                jobs_proprties=_add_jobs_properties_to_list(jobs_proprties,job)        
        message_builder_and_forwarder(jobs_proprties)
    
    
def _add_jobs_properties_to_list(jobs_proprties,job):
    keyr=str(job[0])+':'+str(job[3])+':'+str(job[1])+':'+str(job[10])
    jobs_proprties[job[0]][keyr].append(job[1])#keyword_id 0
    jobs_proprties[job[0]][keyr].append(job[2])#keyword 1
    jobs_proprties[job[0]][keyr].append(job[3])#site_id 2
    jobs_proprties[job[0]][keyr].append(job[4])#site_name 3
    jobs_proprties[job[0]][keyr].append(job[5])#job_detail 4
    jobs_proprties[job[0]][keyr].append(job[6])#email 5
    jobs_proprties[job[0]][keyr].append(job[7])#job_link 6
    jobs_proprties[job[0]][keyr].append(job[8])#post_time 7
    jobs_proprties[job[0]][keyr].append(job[9])#other_info 8
    jobs_proprties[job[0]][keyr].append(job[10])#job_id 9
    jobs_proprties[job[0]][keyr].append(job[0])#subscriber_id 10
    return  jobs_proprties


def message_builder_and_forwarder(message_properties_dictionary):
    for key in message_properties_dictionary:

        msg='''Hello\n\n\n'''
        job_dict=message_properties_dictionary[key]
        count=0
        for ky in job_dict:
            msg=msg+'----------------------------------\n'
            msg=msg+'----------------------------------\n'
            count=count+1
            msg=msg+str(count)+' Site: '+ job_dict[ky][3]+ ' Keyword: '+job_dict[ky][1]+'\n\n'
            msg=msg+'Other info: '+job_dict[ky][8]+'\n\n'
            msg=msg+'Job Link: '+job_dict[ky][6]+'\n\n\n'
            msg=msg+'. '+job_dict[ky][4]+'\n\n\n'
        if(count>0):
            logger.info("Sending jobs") 
            msg=msg+'Kind Regards'
            send_mail(msg,'duncanndiithi@gmail.com',job_dict[ky][5],'Scrapped Data')
        else:
            pass
    if(len(message_properties_dictionary)>0):
        update_sent_jobs(message_properties_dictionary)
    else:
        logger.info("No Jobs to send")
        
            
def update_sent_jobs(message_properties_dictionary):
    logger.info("Updating db on sent items")
    count=0
    for key in message_properties_dictionary:
        job_dict=message_properties_dictionary[key]
        count=count+1
        for ky in job_dict:
            
            try:
                dbUtil = dbConnection()
                cur = dbUtil.get_cursor()
                logger.debug("Updating user_id %d, job_id: %d" %(key,job_dict[ky][9]))
                cur.execute("insert into sent_jobs values(?,?,datetime('now'))", (key,job_dict[ky][9]))
                dbUtil.commit()
            except Exception,e:
                logger.error(e)
            
            
if __name__== "__main__":
    logging.basicConfig(filename='/tmp/jobsscrapper.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("Dispatcher started")
    schedule.every(10).minutes.do(jobs_colletor)

    while True:
        schedule.run_pending()
        time.sleep(1)
        
        
        
        
        