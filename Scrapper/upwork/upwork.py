'''
Created on Sep 14, 2017

@author: duncan
'''
import logging
import sys
sys.path.insert(0, "/home/duncan/workspace/JobsScapper")
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from utils.DBUtils import dbConnection
from items import upwork_item
from items import dao
from random import randint
from Useragent import agent_list
from selenium.webdriver.common.action_chains import ActionChains
import schedule
import time

class upwork:
    
    def __init__(self):
        logger.info("initializing upwork crawler")
        #self.init_url="https://www.upwork.com"
        self.init_url="https://www.upwork.com/o/jobs/browse/c/web-mobile-software-dev/"
        #self.init_url="http://139.59.4.7:8080/"
        #self.chrome_options = webdriver.ChromeOptions()
        #self.chrome_options.add_argument("--headless") 
        #self.chrome_options.add_argument("--window-size=1437,760")
        #self.chrome_options.add_argument("--proxy-server=localhost:8080")
        #self.chrome_options.add_argument("--remote-debugging-port=9222")
        #self.chrome_options.add_argument('--no-sandbox')
        #get user agent
        self.dbUtil = dbConnection()
        self.cur = self.dbUtil.get_cursor()
        self.cur.execute("select user_agent from site where site_id=2")
        data=self.cur.fetchall()
        if len(data)==0 or data[0][0]==None or len(data[0][0])==0:
            print("generating agent")
            index=randint(0,len(agent_list)-1)
            #self.chrome_options.add_argument("--user-agent=%s" %agent_list[index])
            print(agent_list[index])
            #self.cur.execute("update site set user_agent=? where site_id=2", (agent_list[index],))
            self.dbUtil.commit()
        else:
            agnt=""
            for agent in data:
                agnt=agent[0]
            #self.chrome_options.add_argument("--user-agent=%s" %agnt)
            print(agnt)
        #self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.driver = webdriver.Firefox()
        
        try:
            self.dbUtil = dbConnection()
            self.cur = self.dbUtil.get_cursor()
            print("Creating upwork db record")
            self.cur.execute("insert into site(site_id,name) select 2,'Upwork' WHERE NOT EXISTS(SELECT 1 FROM site WHERE site_id = 2 AND name = 'Upwork');  ")
            self.dbUtil.commit()
#             self.cur.execute("select name,value,group_key from cookie where site_id=2")
#             data = self.cur.fetchall()
#             self.dbUtil.commit()
#             logger.info("Cookies; The length: %d" %len(data))
#             if len(data)!=0:
#                 logger.info("cookies exist")
#                 group_set=set()
#                 for d in data:
#                     group_set.add(d[2])
#                 for g_key in group_set:
#                     cookies_dict={}
#                     for d in data:   
#                         if(d[2]==g_key):          
#                             cookies_dict[d[0]]=d[1]
#                     self.driver.add_cookie(cookies_dict)
                
        except Exception as e:
            logger.error(e, exc_info=True)
    
    
    def open_job_listing_page(self):
        logger.info("Making get request to %s " %self.init_url)
        try:
            self.driver.get(self.init_url)
            cookies_dict=self.driver.get_cookies()
            print("\n")
            print("headers")
            print("\n")
            print("Cookies gotten on initial request")
            cookies_dict=self.driver.get_cookies()
            print(cookies_dict)
            #click on the browse button
            #elem = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_css_selector("ul.site-links li.ng-isolate-scope a"))
            #elem.click()
            self.driver.save_screenshot("/tmp/upwrk.png")
            #sleep(1)
            #look for  the Browse Jobs option sub menu
#             elems=self.driver.find_elements_by_css_selector("ul.sub-menu li.tile a.tile-title")
#             print(elems)
#             for e in elems:
#                 print("looking for browse jobs anchor, we have %s" %e.text.lower())
#                 if e.text.lower() == 'Browse Jobs'.lower():
#                     print("element to click is %s " %elem.text)
#                     e.click()
#                     break
            #self.driver.execute_script("document.querySelector('ul.sub-menu li.tile:nth-child(3)').classList.add('active')")
            #WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_css_selector("a[href='/o/jobs/browse/c/web-mobile-software-dev/']")).click()
            #self.driver.save_screenshot("/tmp/upwrk.png")
#             self.dbUtil = dbConnection()
#             self.cur = self.dbUtil.get_cursor()
#             logger.info("searching for cookies")
#             self.cur.execute("select * from cookie where site_id=2")
#             data = self.cur.fetchall()
#             self.dbUtil.commit()
#             logger.info("Cookies; The length: %d" %len(data))
#             if len(data)==0:
#                 logger.info("cookies do not exist, fetching cookies as: ")
#                 
#                 cookies_dict={}
#                 cookies_dict=self.driver.get_cookies()
#                 for count in range(0,len(cookies_dict)):
#                     dict=cookies_dict[count]
#                     for key,val in dict.iteritems():
#                         self.cur.execute("insert into cookie(name,value,site_id,group_key) values('%s','%s',%d,%d)" %(key,val,2,count))
#                         self.dbUtil.commit()
                  
        except (NoSuchElementException, TimeoutException) as e:
            self.driver.save_screenshot("/tmp/upwrk.png")
            logger.error(e, exc_info=True)
            logger.error("Could not find element - ul.site-links li.ng-isolate-scope a - on page {}" %self.driver.current_url)
        except Exception, e:
            self.driver.save_screenshot("/tmp/upwrk.png")
            logger.error("Error while processing request")
            logger.error(e, exc_info=True)
         
        
        
    def search_jobs(self,keywords_to_scrap):
        #keywords_to_scrap={1:'website'}
        self.driver.save_screenshot("/tmp/upwrk.png")
        try:
            for key,attributes_list in keywords_to_scrap.iteritems():
                keywrd=attributes_list[0]
                elem = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_css_selector("#eoFreelancerSearchInput"))
                elem.clear()
                logger.info("Searching keywords in job listing\n")
                logger.info("filtering for %s " %keywrd)
                sleep(20)
                elem.send_keys(keywrd)
                elem.send_keys(Keys.RETURN)
                #parse first page
                sleep(120)
                self.parse_page(key)
                # Navigate through the pagination from results  returned after search
                page_limit=attributes_list[1]
                if page_limit>1:
                    print("Scrolling to page two")
                    visitated_links=[]
                    for i in range(page_limit):
                        #self.driver.execute_script("document.querySelector('footer > div').style.height = '50px'")
                        pagination_list=self.driver.find_elements_by_css_selector("div ul.pagination li a")
#                         for num,next_page in enumerate(pagination_list): 
#                             self.driver.execute_script("document.querySelectorAll('.pagination li')[%d].setAttribute('style', 'display:inline-block !important')" %num)
                        for next_page in pagination_list:
                            
                            if (len(next_page.text.strip())==0 or next_page.text.strip()=='1'):
                                pass
                            else:
                                print("Next page text %s" %str(next_page.text))
                                print("Will compare with %s "%str(i+1))
                                if next_page.text==str(i+1) and next_page.text not in visitated_links:
                                    logger.info("Scrolling to page %s" %str(next_page.text))     
                                    visitated_links.append(next_page.text)
                                    next_page.click()
                                    sleep(120)
                                    self.parse_page(key)
                                    break       
        except TimeoutException, e:
            logger.info("Could not open job listing page to search for keywords")
            counter=self._get_counter()
            logger.info("retry counter at %d "%counter)
            if counter!=1:
                self._increment_counter()
                logger.info("retrying")
                self.dbUtil = dbConnection()
                self.cur = self.dbUtil.get_cursor()
                #self.cur.execute("delete  from cookie where site_id=2")
                self.cur.execute("update site set user_agent=Null where  site_id=2")
                self.dbUtil.commit()
                sleep(120)
                self.tear_down()
                self.__init__()
                self.open_job_listing_page()
                keywords_to_scrap=self.get_subscribed_keywords()
                self.search_jobs(keywords_to_scrap)
                
                
    
    def _get_counter(self):
        self.dbUtil = dbConnection()
        self.cur = self.dbUtil.get_cursor()
        self.cur.execute("select retry from retry_counter where site_id=2")
        data=self.cur.fetchall()
        self.dbUtil.commit()
        counter=0        
        for row in data:
            counter=row[0]
        return counter
    
    def _increment_counter(self):
        self.dbUtil = dbConnection()
        self.cur = self.dbUtil.get_cursor()
        self.cur.execute("delete from retry_counter where site_id=2")
        self.cur.execute("insert into retry_counter(retry,site_id) values(1,2)")
        self.dbUtil.commit()        
    
    def _reset_counter(self):
        self.dbUtil = dbConnection()
        self.cur = self.dbUtil.get_cursor()
        self.cur.execute("delete from retry_counter where site_id=2")
        self.cur.execute("insert into retry_counter(retry,site_id) values(0,2)")
        self.dbUtil.commit()  
        
        
    def parse_page(self,keyword_id):
        
        self.driver.save_screenshot("/tmp/upwrk.png")
        elems= WebDriverWait(self.driver, 20).until(lambda x: x.find_elements_by_css_selector(".job-title-link"))
        
        sleep(15)
        for num,e in enumerate(elems): 
            #makevisible joobs listings   
            self.driver.execute_script("document.querySelectorAll('div.description div span.ng-hide')[%d].setAttribute('style', 'display:block !important')" %num)
        
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
        processd_links=[]
        for dec in titles:
            clss=dec.get_attribute("class")
            if len(dec.text)==0:
                continue
            processed_titles.append(dec.text) 
            processd_links.append(dec.get_attribute('href'))  
         
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
             
        fixed_pay_monitor=0    
        for num,p_desc in enumerate(processed_descriptions):
            item=upwork_item()
            upw_dao=dao()
            item.job_description=p_desc
            item.title=processed_titles[num]
            item.link=processd_links[num]
            item.job_type=processed_jobs_type[num]
            if(item.job_type.lower()=='Fixed-Price'.lower()):
                item.job_payment=processed_jobs_payment[fixed_pay_monitor]
                fixed_pay_monitor=fixed_pay_monitor+1
            else:
                item.job_payment='$$'
            item.job_time_elapse=processed_jobs_time_elapse[num]
            item.keyword_id=keyword_id
            upw_dao.save_item(item)
            
        
    def tear_down(self):
        logger.info("terminating upwork crawler, shutting down web driver")
        self.driver.quit()
       
       
    def get_subscribed_keywords(self):
        sql_query='select distinct(keyword),keyword.keyword_id,max(page_limit) from keyword inner join subscription on subscription.keyword_id=keyword.keyword_id where subscription.site_id=2 group by keyword'
        self.cur.execute(sql_query)
        data = self.cur.fetchall()
        keywordsDict={}
        for row in data:
            attributes_list=[]
            attributes_list.append(row[0])
            attributes_list.append(row[2])
            keywordsDict[row[1]]=  attributes_list
        return keywordsDict

def bootstrap():        
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
        
if __name__== "__main__":
    logging.basicConfig(filename='/tmp/upwork.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("Crawler started")
    schedule.every(5).minutes.do(bootstrap)

    while True:
        schedule.run_pending()
        time.sleep(1)
    
    





        
