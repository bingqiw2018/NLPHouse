#coding=utf-8 
'''
Created on 2018年7月27日

@author: bingqiw
'''
from src.config.Config import Config

class BaseService(object):
    
    param = {}
    
    dao = None
    
    def __init__(self,params={}):
        self.param.update(Config().getConfigParam())
        self.initParam(params)
    
    def initParam(self, params={}, dao=None):
        self.param.update(params)
        self.dao = dao