'''
Created on Sep 14, 2017

@author: duncan
'''
import logging
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from utils.DBUtils import dbConnection
from mock.mock import self
from items import upwork_item
from random import randint
from Useragent import agent_list

class upwork:
    
    def __init__(self):
        logger.info("initializing upwork crawler")
        self.init_url="https://www.upwork.com"
        #self.init_url="http://139.59.4.7:8080/"
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless") 
        self.chrome_options.add_argument("--window-size=1437,760")
        self.chrome_options.add_argument('--no-sandbox')
        #get user agent
        self.dbUtil = dbConnection()
        self.cur = self.dbUtil.getCursor()
        self.cur.execute("select user_agent from site where site_id=2")
        data=self.cur.fetchall()
        if data[0][0]==None or len(data[0][0])==0:
            print("generating agent")
            index=randint(0,len(agent_list)-1)
            self.chrome_options.add_argument("--user-agent=%s" %agent_list[index])
            print(agent_list[index])
            self.cur.execute("update site set user_agent=? where site_id=2", (agent_list[index],))
            self.dbUtil.commit()
        else:
            agnt=""
            for agent in data:
                agnt=agent[0]
            self.chrome_options.add_argument("--user-agent=%s" %agnt)
            print(agnt)
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        
        
        try:
            self.dbUtil = dbConnection()
            self.cur = self.dbUtil.getCursor()
            print("Creating upwork db record")
            self.cur.execute("insert into site(site_id,name) select 2,'Upwork' WHERE NOT EXISTS(SELECT 1 FROM site WHERE site_id = 2 AND name = 'Upwork');  ")
            self.dbUtil.commit()
            self.cur.execute("select name,value,group_key from cookie where site_id=2")
            data = self.cur.fetchall()
            self.dbUtil.commit()
            logger.info("Cookies; The length: %d" %len(data))
            if len(data)!=0:
                logger.info("cookies exist")
                group_set=set()
                for d in data:
                    group_set.add(d[2])
                for g_key in group_set:
                    cookies_dict={}
                    for d in data:   
                        if(d[2]==g_key):          
                            cookies_dict[d[0]]=d[1]
                    self.driver.add_cookie(cookies_dict)
                
        except Exception as e:
            logger.error(e, exc_info=True)
    
    
    def open_job_listing_page(self):
        logger.info("Making get request to %s " %self.init_url)
        try:
            self.driver.get(self.init_url)
            #click on the browse button
            elem = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_css_selector("ul.site-links li.ng-isolate-scope a"))
            elem.click()
            self.driver.save_screenshot("/tmp/upwrk.png")
            sleep(1)
            #look for  the Browse Jobs option sub menu
#             elems=self.driver.find_elements_by_css_selector("ul.sub-menu li.tile a.tile-title")
#             print(elems)
#             for e in elems:
#                 print("looking for browse jobs anchor, we have %s" %e.text.lower())
#                 if e.text.lower() == 'Browse Jobs'.lower():
#                     print("element to click is %s " %elem.text)
#                     e.click()
#                     break
            self.driver.execute_script("document.querySelector('ul.sub-menu li.tile:nth-child(3)').classList.add('active')")
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_css_selector("a[href='/o/jobs/browse/c/web-mobile-software-dev/']")).click()
            self.driver.save_screenshot("/tmp/upwrk.png")
            self.dbUtil = dbConnection()
            self.cur = self.dbUtil.getCursor()
            logger.info("searching for cookies")
            self.cur.execute("select * from cookie where site_id=2")
            data = self.cur.fetchall()
            self.dbUtil.commit()
            logger.info("Cookies; The length: %d" %len(data))
            if len(data)==0:
                logger.info("cookies do not exist, fetching cookies as: ")
                
                cookies_dict={}
                cookies_dict=self.driver.get_cookies()
                for count in range(0,len(cookies_dict)):
                    dict=cookies_dict[count]
                    for key,val in dict.iteritems():
                        self.cur.execute("insert into cookie(name,value,site_id,group_key) values('%s','%s',%d,%d)" %(key,val,2,count))
                        self.dbUtil.commit()
                  
        except (NoSuchElementException, TimeoutException) as e:
            self.driver.save_screenshot("/tmp/upwrk.png")
            logger.error(e, exc_info=True)
            logger.error("Could not find element - ul.site-links li.ng-isolate-scope a - on page {}" %self.driver.current_url)
        except Exception, e:
            self.driver.save_screenshot("/tmp/upwrk.png")
            logger.error("Error while processing request")
            logger.error(e, exc_info=True)
         
        
        
    def search_jobs(self,keywords_to_scrap):
        keywords_to_scrap={1:'article'}
        self.driver.save_screenshot("/tmp/upwrk.png")
        try:
            elem = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_css_selector("#eoFreelancerSearchInput"))
            elem.clear()
            logger.info("Searching keywords in job listing\n")
            for key,keywrd in keywords_to_scrap.iteritems():
                logger.info("filtering for %s " %keywrd)
                elem.send_keys(keywrd)
                elem.send_keys(Keys.RETURN)
                elems= WebDriverWait(self.driver, 20).until(lambda x: x.find_elements_by_css_selector(".job-title-link"))
                self.driver.save_screenshot("/tmp/upwrk.png")
                for num,e in enumerate(elems):    
                    self.driver.execute_script("document.querySelectorAll('div.description div span.ng-hide')[%d].setAttribute('style', 'display:block !important')" %num)
                
                self.parse_page()
        except TimeoutException, e:
            logger.info("Could not open job listing page to search for keywords")
            counter=self._get_counter()
            logger.info("retry counter at %d "%counter)
            if counter!=1:
                self._increment_counter()
                logger.info("retrying")
                self.dbUtil = dbConnection()
                self.cur = self.dbUtil.getCursor()
                self.cur.execute("delete  from cookie where site_id=2")
                self.cur.execute("update site set user_agent=Null where  site_id=2")
                self.dbUtil.commit()
                sleep(60)
                self.tear_down()
                self.__init__()
                self.open_job_listing_page()
                keywords_to_scrap=upw.get_subscribed_keywords()
                self.search_jobs(keywords_to_scrap)
                
                
    
    def _get_counter(self):
        self.dbUtil = dbConnection()
        self.cur = self.dbUtil.getCursor()
        self.cur.execute("select retry from retry_counter where site_id=2")
        data=self.cur.fetchall()
        self.dbUtil.commit()
        counter=0        
        for row in data:
            counter=row[0]
        return counter
    
    def _increment_counter(self):
        self.dbUtil = dbConnection()
        self.cur = self.dbUtil.getCursor()
        self.cur.execute("delete from retry_counter where site_id=2")
        self.cur.execute("insert into retry_counter(retry,site_id) values(1,2)")
        self.dbUtil.commit()        
    
    def _reset_counter(self):
        self.dbUtil = dbConnection()
        self.cur = self.dbUtil.getCursor()
        self.cur.execute("delete from retry_counter where site_id=2")
        self.cur.execute("insert into retry_counter(retry,site_id) values(0,2)")
        self.dbUtil.commit()  
        
    def parse_page(self):
        from decorator import append
        #item=upwork_item()
        
        descriptions=self.driver.find_elements_by_css_selector("div.description div span.ng-hide span")
        titles=self.driver.find_elements_by_css_selector("div div h4 a.job-title-link")
        jobs_type=self.driver.find_elements_by_css_selector("div div small strong.js-type")
        jobs_payment=self.driver.find_elements_by_css_selector("div div span.js-budget span")
        jobs_time_elapse=self.driver.find_elements_by_css_selector("div div small span.js-posted time")
        
        processed_descriptions=[]
        for dec in descriptions:
            clss=dec.get_attribute("class")
            if clss=="highlight" or len(dec.text)==0:
                continue
            print(dec.text)
            processed_descriptions.append(dec.text)
            
        processed_titles=[]   
        for dec in titles:
            clss=dec.get_attribute("class")
            if len(dec.text)==0:
                continue
            processed_titles.append(dec.text)   
        
        processed_jobs_type=[]
        for dec in jobs_type:
            clss=dec.get_attribute("class")
            if len(dec.text)==0:
                continue
            processed_jobs_type.append(dec.text) 
         
        processed_jobs_payment=[]    
        for dec in jobs_payment:
            clss=dec.get_attribute("class")
            if clss=="highlight" or len(dec.text)==0:
                continue
            processed_jobs_payment.append(dec.text) 
            
        processed_jobs_time_elapse=[]    
        for dec in jobs_time_elapse:
            clss=dec.get_attribute("class")
            if len(dec.text)==0:
                continue
            processed_jobs_time_elapse.append(dec.text)
            
        
        
    def tear_down(self):
        logger.info("terminating upwork crawler, shutting down web driver")
        self.driver.quit()
       
       
    def get_subscribed_keywords(self):
        
        logger.info("fetching keywords to scrap")
        self.cur.execute("select keyword_id from site_keyword where site_id=2")
        data = self.cur.fetchall()
        keywordsSet=set()
        for row in data:
            keywordsSet.add(row[0])
        sql_query='select * from keyword where keyword_id in (' + ','.join((str(n) for n in keywordsSet)) + ') '
        print(sql_query)
        self.cur.execute(sql_query)
        data = self.cur.fetchall()
        keywordsDict={}
        for row in data:
            keywordsDict[row[0]]=row[1]
        return keywordsDict
        

if __name__== "__main__":
    logging.basicConfig(filename='/tmp/upwork.log', filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("Crawler started")
    upw=upwork()
    try:
        upw.open_job_listing_page()
        keywords_to_scrap=upw.get_subscribed_keywords()
        upw.search_jobs(keywords_to_scrap)
    except Exception as e:
        print(e)
        logger.error(e, exc_info=True)
    finally:
        upw.tear_down()
        upw._reset_counter()





        
