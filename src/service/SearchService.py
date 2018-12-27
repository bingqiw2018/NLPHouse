#coding=utf-8 
'''
Created on 2018年7月15日

@author: bingqiw
'''
import os
from src.dao.SearchDao import SearchDao
import src.utils.DateUtils as du
from BaseService import BaseService

class SearchService(BaseService):
    
    def initParam(self, params={}, dao=None):
        BaseService.initParam(self, params, SearchDao())
        
    def doSearchLearn(self):
        
        try:
            param = {
                'session_id':du.get_unit_id(),
                'words':self.param['domain_name'],
                'create_time':du.current_time(),
                'other_id':self.param['spider']['search_spider']
                }
            print "增加一条会话记录："+str(param['words'])
            self.dao.addSessionKeywords(param)
            
            print "数据抓取开始 ..."
#             scrapy.cmdline.execute(argv=['scrapy','crawl',self.__spider])  
            os.system("scrapy crawl "+self.param['spider']['search_spider'])
            print "数据抓取，结束！"
        finally:
            print ""        