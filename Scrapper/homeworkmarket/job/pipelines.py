# -*- coding: utf-8 -*-
import  sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from __builtin__ import str
import logging

from scrapy.exporters import JsonItemExporter, CsvItemExporter
from scrapy.mail import MailSender

from utils.DBUtils import dbConnection


logging.basicConfig(filename='/tmp/homeworkMarket.log', filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class JobsFilter(object):
   
    def __init__(self):
        logger.info ("Initializing sequence")
        self.con = None
        self.dbUtil = dbConnection()
        self.cur = self.dbUtil.get_cursor()
        self.mesgBody = ''' 
        Hi Duncan,
        
            We found the following jobs that we Think might be Interesting to you.
            Please Check them out.
        
        Kind Regards,
        Duncan.
        '''
        self.waks = open("waks.csv", 'wb')
        self.exporter = CsvItemExporter(self.waks, unicode)
        self.exporter.start_exporting()
        try:
            self.cur.execute("insert into site(site_id,name) values(1,'HomeWork Market')")
            self.dbUtil.commit()
        except:
            pass
        
        
    def process_item(self, item, spider):
          
        try: 
            self.cur.execute("insert into jobs(detail,time_created,site_id) values('%s',datetime('now'),1)" % item['name'])
            self.dbUtil.commit()
            self.exporter.export_item(item)
        except Exception as e: 
            logger.error(e)
        return item
  
  
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        credFile = open("cred.txt", "r")
        cred = []
        for line in credFile:
            cred.append(line)
        u = str.split(cred[0], '|')
        p = str.split(cred[1], '/')
        un = self.unMar(u[0]) + self.unMar(u[1].rstrip())
        ps = self.unMar(p[0]) + self.unMar(p[1])
        credFile.close()
        
        self.cur.execute("select keyword from keyword")
        keyWordList = []
        keywords = self.cur.fetchall()
        for keyword in keywords:
            keyWordList.append(keyword[0])
            print (keyword[0])  
        
        self.cur.execute("select detail,job_id from jobs where status=0")
        jobs = self.cur.fetchall()
        jobsList = []
        jobIdList = set()
        for job in jobs:
            for keyword in keyWordList:
                if keyword in job[0]:
                    jobsList.append(job[0])
                    jobIdList.add(job[1])
         
        if(len(jobsList) > 2):
            myFile = open("waks.txt", "wb")
            myFile.write("Following Jobs Seems Interesting\n")
            for x in range(0, len(jobsList)):
                strn = str(x + 1) + " " + jobsList[x].encode("utf-8", "strict") + "\n"
                myFile.write(strn)
            myFile.close()
            myFile = open("waks.txt", "r")
            mailer = MailSender(smtphost="smtp.gmail.com", mailfrom=un, smtpuser=un, smtppass=ps, smtpport=587)
            ids = (", ".join(str(e) for e in jobIdList))
            mailer.send(to=[un], subject="Scrapy mail", body=self.mesgBody, attachs=(("HomeWork Ma", "text/plain", myFile),))
            sqlStr = str("update jobs set status=1 where job_id IN (%s)" % ids)
            logger.info(sqlStr)
            self.cur.execute(sqlStr)
            self.dbUtil.commit()            
        self.waks.close()
        logger.info("Terminating sequence") 
        try:
            self.dbUtil.close_db_connection()
        except Exception as e:
            print(e)
            
    
    def unMar(self, stri):
        x = str(stri)
        decValue = ''
        valRv = ''
        for y in range(len(x) - 1, -1, -1):
            valRv = valRv + x[y]    
        for y in range(0, len(valRv)):
                decValue = decValue + chr(ord(valRv[y]) - y)
        return decValue
    



class HomeWorkMarket(object):

    def __init__(self):
        self.file = open("jobs.json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()
 
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
 
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    

class HomeWorkMarketCsv(object):
    
    def __init__(self):
        self.file = open("jobs.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, unicode)
        self.exporter.start_exporting()
 
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        # usinf gmail to send mail
        mailer = MailSender(smtphost="smtp.gmail.com", mailfrom='', smtpuser="", smtppass="", smtpport=587)
        myFile = open("jobs.csv", "r")
        self.file.close()
        mailer.send(to=["duncanndiithi@gmail.com"], subject="Scrapy mail", body="Did you receive this, oh!", attachs=(("twors", "text/plain", myFile),))
        
 
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
