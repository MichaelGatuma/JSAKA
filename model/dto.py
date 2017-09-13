'''
Created on Aug 7, 2017

@author: duncan
'''
from email import email


class Subscriber(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
        

class Subscription():
    
    def __init__(self, email, sites, keywords, subId):
        '''
        Constructor
        '''
        self.subId = subId
        self.email = email
        self.sites = sites
        self.keywords = keywords
    
    def getSubId(self):
        return self.subId
    def getMail(self):
        return self.email
    def getSite(self):
        return self.sites
    def getKeywords(self):
        return self.keywords
    
       
    
