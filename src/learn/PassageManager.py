#coding=utf-8 
'''
Created on 2018年8月6日

@author: bingqiw
'''

from BaseManager import BaseManager
from src.service.PassageService import PassageService
from src.service.NLService import NLService

class PassageManager(BaseManager):

    def getLearnRequest(self):
        print "获得熟知学习需求，开始..."
        request = []
#         查看媒体目录需要学习的文章
        flag = NLService().getDocPsgForPsgLearn(self.param)
        request.append({'isLearn':flag})
        self.param['request'] = request    
    
    def startLearn(self):
        print "开始学习 ..."
        
        self.getLearnRequest()
        
        if self.param['request'][0]['isLearn'] == False:
            print "学习需求无效 ..."
        else:
            nls = NLService()
            if nls.doLdaPsgLearn(self.param) :
                ps = PassageService()
                flag = ps.createCognitionPassages(self.param)
                
        print "学习结束！"