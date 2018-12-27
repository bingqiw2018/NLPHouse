#coding=utf-8 
'''
Created on 2018年7月6日

@author: bingqiw
'''

from src.service.ConceptService import ConceptService
from BaseManager import BaseManager
 
class ConceptManager(BaseManager):
    
    def initParam(self, params={}):
        if params.has_key('domain_name'):
            self.param.update({
                'domain_name':params['domain_name'], 
                'keyword':params['domain_name']
            })
            
    '''
    定义学习概念类，用来识别段落是否是定义类内容。
    '''
    def refreshConcept(self,param): 
        cs = ConceptService(param)
        cs.refreshConcept()
        
    #     创建领域概念结点，注意结点初始化，并不包括内容
    def createDomainConcept(self,param):
        cs = ConceptService()
        cs.createDomainConcept(param)    
        
        
    def getLearnRequest(self):
        pass 
    
    def startLearn(self): 
        cs = ConceptService(self.param)
        cs.refreshConcept()
