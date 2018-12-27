#coding=utf-8 
'''
Created on 2018年7月25日

@author: bingqiw
'''
from src.datasource.DBManager import DBManager

class BaseDao(object):
    
    db = None
    
    def __init__(self):
        self.db = DBManager()
