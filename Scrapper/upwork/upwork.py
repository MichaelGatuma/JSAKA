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

class upwork:
    
    def __init__(self):
        logger.info("initializing upwork crawler")
        self.init_url="https://www.upwork.com"
        #self.init_url="http://139.59.4.7:8080/"
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless") 
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0")
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.dbUtil = dbConnection()
        self.cur = self.dbUtil.getCursor()
        
        try:
            print("inserting upwork")
            self.cur.execute("insert into site(site_id,name) select 2,'Upwork' WHERE NOT EXISTS(SELECT 1 FROM site WHERE site_id = 2 AND name = 'Upwork');  ")
            self.dbUtil.commit()
        except Exception as e:
            logger.error(e, exc_info=True)
    
    def set_up(self):
        logger.info("Making get request to %s " %self.init_url)
        try:
            self.driver.get(self.init_url)
            elem = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_css_selector("ul.site-links li.ng-isolate-scope a"))
            elem.click()
            self.driver.save_screenshot("/tmp/upwrku.png")
            sleep(1)
            self.driver.save_screenshot("/tmp/upwrku.png")
            elems=self.driver.find_elements_by_css_selector("ul.sub-menu li.tile a.tile-title strong")
            print(elems)
            for e in elems:
                print(e.text.lower())
                if e.text.lower() == 'Browse Jobs'.lower():
                    e.click()
                    break
            self.driver.save_screenshot("/tmp/upwrku.png")
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_css_selector("a[href='/o/jobs/browse/c/web-mobile-software-dev/']")).click()
            
        except (NoSuchElementException, TimeoutException) as e:
            self.driver.save_screenshot("/tmp/upwrku.png")
            logger.error(e, exc_info=True)
            logger.error("Could not find element - ul.site-links li.ng-isolate-scope a - on page {}" %self.driver.current_url)
        except Exception, e:
            self.driver.save_screenshot("/tmp/upwrku.png")
            logger.error("Error while processing request")
            logger.error(e, exc_info=True)
         
        
        
    def parse(self):
        self.driver.save_screenshot("/tmp/upwrku.png")
        elem = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_css_selector("#eoFreelancerSearchInput"))
        elem.clear()
        logger.info("Searching for scrap")
        elem.send_keys("scrap")
        elem.send_keys(Keys.RETURN)
        logger.info("selecting job description") 
        elems= WebDriverWait(self.driver, 10).until(lambda x: x.find_elements_by_css_selector(".job-title-link"))
        print(elems)
        
        for num,e in enumerate(elems):    
            self.driver.execute_script("document.querySelectorAll('div.description div span.ng-hide')[%d].setAttribute('style', 'display:block !important')" %num)

        self.driver.save_screenshot("/tmp/upwrku.png")
        
        
    def crawl(self):
        pass
    
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
        
        

if __name__== "__main__":
    logging.basicConfig(filename='/tmp/upwork.log', filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("Crawler started")
    upw=upwork()
    try:
        
        upw.set_up()
        upw.parse()
        upw.get_subscribed_keywords()
    except Exception as e:
        print(e)
        logger.error(e, exc_info=True)
    finally:
        upw.tear_down()





        
