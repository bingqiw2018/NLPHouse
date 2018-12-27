#coding=utf-8 
'''
Created on 2018年7月15日

@author: bingqiw
'''
import scrapy.cmdline 
import os
from src.dao.MediaDao import MediaDao
from BaseService import BaseService

class MediaService(BaseService):
    
    #未学习的媒体号
    REQUEST_LEARN_TYPE_UNLEARN = 0
    
    #单独媒体号主页
    REQUEST_LEARN_TYPE_ONLY_MEDIA = 1
    
    #当天媒体号
    REQUEST_LEARN_TYPE_TODAY = 2
    
    __spider = None
    
    def initParam(self, params={}, dao=None):
        BaseService.initParam(self, params, MediaDao())
        
    def doMediaLearn(self):
        
        param = self.param
        
        learn_type = param['learn_type']
        
        if learn_type == self.REQUEST_LEARN_TYPE_UNLEARN:
            self.__spider = self.param['spider']['media_unlearn_spider']
        elif learn_type == self.REQUEST_LEARN_TYPE_ONLY_MEDIA:
            self.__spider =  self.param['spider']['media_only_spider']
        elif learn_type == self.REQUEST_LEARN_TYPE_TODAY:
            self.__spider =  self.param['spider']['media_today_spider']
        print "爬虫选择："+self.__spider
        try:
            print "数据抓取..."
#             scrapy.cmdline.execute(argv=['scrapy','crawl',self.__spider])  
            os.system("scrapy crawl "+self.__spider)
            print "数据抓取，结束！"
        finally:
            print ""   
    
    