#coding=utf-8 
'''
Created on 2018年7月11日

@author: bingqiw
'''

from CognitionManager import CognitionManager
from src.service.MediaService import MediaService

class CognitionDriver(object):
    
#    指导性认知学习:创建领域结点，总结领域的高频词汇及对应的概念词汇；初始化领域对应的概念结点
#    参数param说明：
#         domain_name：领域关键字
    def learnCognitionByGuide(self, param):
        cm = CognitionManager()
        cm.getGuideCognition(param).startLearn()

#     自主学习-搜索学习

#   参数：domain_name = 搜索关键字，目前都是指定领域
    def searchCognitionBySelf(self,param):
        
        cm = CognitionManager()
        
        param['search_cognition'] = True
#         搜索指定领域词汇    
        cm.getOwnCognition(param).startLearn()
    
#         认知学习开始，领域学习
        param['guide_learn_type'] = 'domain'
        cm.getGuideCognition(param).startLearn()
         
#         概念学习学习
        param['guide_learn_type'] = 'concept'
        cm.getGuideCognition(param).startLearn()
          
#         自主学习--媒体学习
    def mediaCognitionBySelf(self,param):
        
        cm = CognitionManager()
        
        param['media_cognition'] = True
        param['learn_type'] = MediaService.REQUEST_LEARN_TYPE_TODAY   
#         搜索指定领域词汇    
#         cm.getOwnCognition(param).startLearn()
        
#         认知学习开始，领域学习
        param['guide_learn_type'] = 'media'
        cm.getGuideCognition(param).startLearn()
        
#         param['guide_learn_type'] = 'domain'
#         cm.getGuideCognition(param).refreshDomain(param)
