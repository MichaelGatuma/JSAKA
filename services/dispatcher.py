'''
Created on Nov 14, 2017

@author: duncan
'''
import logging
import schedule
import time
from utils.DBUtils import dbConnection
from utils.mail import send_mail
from macpath import curdir
from pipelines import logger

        
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
                        kyword.keyword as keyword,tt1.site_id as site_id,syt.name as site_name,
                        tt1.detail as job_detail,subsc.email as email,tt1.link as job_link,
                        tt1.time_created as post_time,tt1.other_info as other_info,tt1.job_id as job_id from 
                        (select sab.minimum_alert as jobs_no,sab.subscriber_id,sab.site_id,sab.keyword_id,
                        jb.detail,jb.job_id,jb.link,jb.time_created,jb.other_info
                        from subscription as sab,jobs as jb) tt1
                        inner join
                        (select count(*) as jobs_no,jobo.keyword_id as keyword_id,jobo.site_id as site_id,jobo.job_id from jobs jobo 
                        inner join subscription subs on subs.site_id=jobo.site_id and subs.keyword_id=jobo.keyword_id
                        inner join subscriber subscrib on subscrib.subscriber_id=subs.subscriber_id  
                        group by subscrib.email,jobo.keyword_id,jobo.site_id) tt2 
                        on tt1.site_id=tt2.site_id  and tt1.keyword_id=tt2.keyword_id and tt1.job_id=tt2.job_id
                        inner join subscriber subsc on tt1.subscriber_id=subsc.subscriber_id
                        inner join site syt on tt1.site_id=syt.site_id
                        inner join keyword kyword on tt1.keyword_id=kyword.keyword_id
                        where tt1.jobs_no<=tt2.jobs_no and not exists (select 1 from sent_jobs where    tt1.subscriber_id=subscriber_id and tt1.job_id=job_id)
                        group by tt1.subscriber_id,tt1.keyword_id,tt1.site_id,tt1.job_id'''
    logger.info("Collecting jobs")
    cur.execute(jobs_to_dispatch) 
    data_to_dispatch = cur.fetchall()
    if(data_to_dispatch!=None or len(data_to_dispatch)!=0):
        jobs_proprties={}
        for job in data_to_dispatch:
            keyr=str(job[0])+':'+str(job[3])+':'+str(job[1])
            try:
                jobs_proprties[job[0]]
            except KeyError,e:
                logger.debug(e)
                jobs_proprties[job[0]]={}
           
            try:
                jobs_proprties[job[0]][keyr]
                jobs_proprties=_add_jobs_properties_to_list(jobs_proprties,job)
            except KeyError,e:
                logger.info(e)
                jobs_proprties[job[0]][keyr]=[]
                jobs_proprties=_add_jobs_properties_to_list(jobs_proprties,job)        
    message_builder_and_forwarder(jobs_proprties)
    
    
def _add_jobs_properties_to_list(jobs_proprties,job):
    keyr=str(job[0])+':'+str(job[3])+':'+str(job[1])
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
        else:
            logger.info("No Jobs to send")
        msg=msg+'Kind Regards'
        send_mail(msg,'sender',job_dict[ky][5],'Scrapped Data')    
    update_sent_jobs(message_properties_dictionary)
        
            
def update_sent_jobs(message_properties_dictionary):
    for key in message_properties_dictionary:
        job_dict=message_properties_dictionary[key]
        for ky in job_dict:
            try:
                dbUtil = dbConnection()
                cur = dbUtil.get_cursor()
                cur.execute("insert into sent_jobs values(?,?)", (job_dict[ky][10],job_dict[ky][9]),"datetime('now')")
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
        
        
        
        
        