#coding=utf-8 
'''
Created on 2018年7月15日

@author: bingqiw
'''
from DomainManager import DomainManager, DomainMediaManager
from ConceptManager import ConceptManager
from SearchManager import SearchManager
from MediaManager import MediaManager
from BaseManager import BaseManager
from PassageManager import PassageManager

class CognitionManager(BaseManager):
    
    def getGuideCognition(self, param):
        
        if param.has_key('guide_learn_type') and param['guide_learn_type'] == 'domain' :
            return DomainManager(param)
        elif param.has_key('guide_learn_type') and param['guide_learn_type'] == 'concept' :
            return ConceptManager(param)
        elif param.has_key('guide_learn_type') and param['guide_learn_type'] == 'media' :
            return DomainMediaManager(param)
        elif param.has_key('guide_learn_type') and param['guide_learn_type'] == 'passage' :
            return PassageManager(param)
        
    def getOwnCognition(self,param):
        
        if param.has_key('search_cognition'):
            return SearchManager(param)
            
        elif param.has_key('media_cognition'):
            return MediaManager(param)
        
        else:
            print "自主学习没有指令"