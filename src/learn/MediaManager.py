#coding=utf-8 
'''
Created on 2018年7月15日

@author: bingqiw
'''
from BaseManager import BaseManager
from src.service.MediaService import MediaService

class MediaManager(BaseManager):
    #未学习的媒体号
    REQUEST_LEARN_TYPE_UNLEARN = 0
    #单独媒体号主页
    REQUEST_LEARN_TYPE_ONLY_MEDIA = 1
    #当天媒体号
    REQUEST_LEARN_TYPE_TODAY = 2
    
    def getLearnRequest(self):
        
        param = self.param
        
        if len(param)>0 and param.has_key('learn_type'):
            learn_type = param['learn_type']
            request = {'learn_type':learn_type}
            self.param['request']  = request 
        else:
            print "Not found learn_type:"     
                
                   
    def startLearn(self):
        
        self.getLearnRequest()
        
        param = self.param
        ms = MediaService(param)
        ms.doMediaLearn()    
        
