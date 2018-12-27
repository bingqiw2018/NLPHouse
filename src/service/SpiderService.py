#coding=utf-8 
'''
Created on 2018年7月14日

@author: bingqiw
'''

from src.dao.SpiderDao import SpiderDao
from BaseService import BaseService

class SpiderService(BaseService):
    
    def initParam(self, params={}, dao=None):
        BaseService.initParam(self, params, SpiderDao())
        
    def getMediaCatalogs(self, doc_list):
        self.dao.getMediaCatalogs(doc_list)
            
    def getDocCatalogs(self,doc_list):
        self.dao.getDocCatalogs(doc_list)
    
    def querySessionKeywords(self,param):    
        return self.dao.querySessionKeywords(param)
    
    def queryToutiaoMediaUserUnDone(self,param):   
        return self.dao.queryToutiaoMediaUserUnDone(param) 
    
    def queryToutiaoMediaUser(self,param):   
        return self.dao.queryToutiaoMediaUser(param)
    
    def queryDocCatalogsWithoutPassages(self,param):
        return self.dao.queryDocCatalogsWithoutPassages(param)
    
    def getDocPassages(self,param):
        return self.dao.getDocPassages(param)