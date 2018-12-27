#coding=utf-8 
'''
Created on 2018年7月11日

@author: bingqiw
'''
from src.service.NLService import NLAnalysis
from BaseManager import BaseManager

class NLManager(BaseManager):
    
    def LdaAnalysis(self, param):
        la = NLAnalysis()
        la.analyseLdaByTitle(param)
    
