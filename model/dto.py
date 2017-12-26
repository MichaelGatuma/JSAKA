'''
Created on Aug 7, 2017

@author: duncan
'''



class Subscriber(object):
    def __init__(self, subscriber_id, subscriber_email):
        self.subscriber_id = subscriber_id
        self.subscriber_email = subscriber_email
        

class Site(object):
    def __init__(self, site_id, site_name):
        self.site_id = site_id
        self.site_name = site_name


class Keyword(object):
    def __init__(self, keyword_id, keyword_name):
        self.keyword_id = keyword_id
        self.keyword_name = keyword_name
       
       
class Subscription():
    
    def __init__(self, site, keyword,  subscription_group_id=None, subscriber=None, page_limit=1, minimum_alert=1):
        '''
        Constructor
        '''
        self.subscriber = subscriber
        self.site = site
        self.keyword = keyword
        self.page_limit = page_limit
        self.minimum_alert = minimum_alert
        self.subscription_group_id = subscription_group_id
        
