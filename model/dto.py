'''
Created on Aug 7, 2017

@author: duncan
'''

from mock.mock import self


class Subscriber(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
        

class Subscription():
    
    def __init__(self, subscriber_email, site_id, keyword_id, subscriber_id,page_limit,minimum_alert,subscription_group_id):
        '''
        Constructor
        '''
        self.subscriber_id = subscriber_id
        self.site_id = site_id
        self.keyword_id = keyword_id
        self.page_limit=page_limit
        self.minimum_alert=minimum_alert
        self.subscription_group_id=subscription_group_id
        self.subscriber_email=subscriber_email
