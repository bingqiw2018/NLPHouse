#coding=utf-8 
'''
Created on 2018年7月15日

@author: bingqiw
'''
from src.config.Config import Config


class BaseManager(object):
    
    param = {}
    
    def __init__(self,params={}):
        
        self.param.update(Config().getConfigParam())
        if params != None:
            self.initParam(params)
    
    def initParam(self, params={}):
        self.param.update(params)
        
    def getLearnRequest(self):
        pass
    
    def startLearn(self):
        pass