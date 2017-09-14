'''
Created on Sep 14, 2017

@author: duncan
'''
from selenium import webdriver
from time import sleep

class upwork:
    
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless") 
        self.chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        sleep(4)
        pass
    
    def set_up(self):
        pass
    
    def parse(self):
        pass
    
    def crawl(self):
        pass
    
    def tear_down(self):
        pass