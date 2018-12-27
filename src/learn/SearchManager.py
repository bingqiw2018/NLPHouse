#coding=utf-8 
'''
Created on 2018年7月15日

@author: bingqiw
'''

from BaseManager import BaseManager

from src.service.SearchService import SearchService

class SearchManager(BaseManager):
    
    def initParam(self, params={}):
        self.param.update(params)  
        
    def getLearnRequest(self):
        #不接受前向指定参数
        request = {
                'spider':self.param['spider']['search_spider'],
                'domain_name':self.param['domain_name']
            }
        
        self.param['request'] = request
    
    
    def startLearn(self):
        
        self.getLearnRequest()
        
        print "即时搜索学习,开始..."
        ss = SearchService(self.param)
        ss.doSearchLearn()
        
