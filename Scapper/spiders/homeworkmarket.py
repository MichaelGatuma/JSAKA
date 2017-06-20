# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import json
from Scapper.items import jobName

class HomeworkmarketSpider(scrapy.Spider):
    name = 'homeworkmarket'
    allowed_domains = ["homeworkmarket.com"]
  #  start_urls = ["https://www.homeworkmarket.com/all/register/login"]   
    start_urls = ["https://www.homeworkmarket.com/views/ajax?field_is_tutorial_value_many_to_one=0&tid=17&quid=&view_name=all_questions&view_display_id=page_4&view_args=&view_path=homework-answers&view_base_path=questions%2Fsearch&view_dom_id=1&pager_element=0",                  
                  "https://www.homeworkmarket.com/views/ajax?js=1&page=1&field_is_tutorial_value_many_to_one=0&tid=17&view_name=all_questions&view_display_id=page_4&view_path=homework-answers&view_base_path=questions%2Fsearch&view_dom_id=2&pager_element=0&view_args="]
    
    def parse(self,response):
        content=json.loads(response.body)
        body = '<html><body>'+content['display']+'</html></body>'
        jobDesc=Selector(text=body).css("td.views-field a::text").extract()
        jbName=jobName()
        for task in jobDesc:
            if "Computer Science homework help" not in task:
                jbName['name']=task
                yield jbName
    
    
    
    
    
    
    
    
    
    
    
    
    def Login(self, response):
        ''' 
            Log in to Homework market.com and return response object
            from_response() <--- method simulated click on login form 
        '''
        return scrapy.FormRequest.from_response(
            response,
            formdata={'name': '', 'pass': ''},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "unrecognized username or password" in response.body:
            self.logger.error("Login failed")
            return
        else:
            next_page = response.css('li:nth-child(2).leaf a::attr(href)').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.processJobs)
                    
                