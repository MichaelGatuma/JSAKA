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
from bs4 import BeautifulSoup as soup

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
        
        sleep(4)
        
    
    def set_up(self):
        upworkDriver=self.driver
        logger.info("Making get request to %s " %self.init_url)
        try:
            upworkDriver.get(self.init_url)
            elem = WebDriverWait(upworkDriver, 10).until(lambda x: x.find_element_by_css_selector("ul.site-links li.ng-isolate-scope a"))
            elem.click()
            upworkDriver.save_screenshot("/tmp/clickOnDropDownMenu.png")
            self.driver.find_element_by_css_selector("li.tile:nth-child(3) > a:nth-child(1)").click()
            sleep(1)
            self.driver.find_element_by_css_selector("li.tile:nth-child(3) > ul:nth-child(2) > li:nth-child(1) > a:nth-child(1)").click()
            elem = WebDriverWait(upworkDriver, 10).until(lambda x: x.find_element_by_css_selector("#eoFreelancerSearchInput"))
            elem.clear()
            elem.send_keys("scrap")
            elem.send_keys(Keys.RETURN)
            
            upworkDriver.save_screenshot("/tmp/clickOnDropDownMenu.png")
        except (NoSuchElementException, TimeoutException) as e:
            upworkDriver.save_screenshot("/tmp/clickOnDropDownMenu.png")
            logger.error(e, exc_info=True)
            logger.error("Could not find element - ul.site-links li.ng-isolate-scope a - on page {}" %upworkDriver.current_url)
        except Exception, e:
            upworkDriver.save_screenshot("/tmp/clickOnDropDownMenu.png")
            logger.error("Error while processing request")
            logger.error(e, exc_info=True)
         
        
        
    def parse(self, html):
        content=soup("lxml",html)
        
    def crawl(self):
        pass
    
    def tear_down(self):
        logger.info("terminating upwork crawler")
        self.driver.quit()
       
        
        
        

if __name__== "__main__":
    logging.basicConfig(filename='/tmp/upwork.log', filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("Crawler started")
    try:
        upw=upwork()
        upw.set_up()
       
    except Exception as e:
        print(e)
        logger.error(e, exc_info=True)
    finally:
        upw.tear_down()





        