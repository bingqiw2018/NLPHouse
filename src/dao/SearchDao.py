#coding=utf-8 
'''
Created on 2018年7月16日

@author: bingqiw
'''
from BaseDao import BaseDao

class SearchDao(BaseDao):
    
    def addSessionKeywords(self, param):
        
        sql = "insert nl_session_words (session_id,words,create_time,other_id) VALUES (%s,%s,%s,%s)    "
        arr = []
         
        arr.append([param['session_id'],param['words'],param['create_time'],param['other_id']])
            
        flag = self.db.batch_sql(sql,arr)
        print "入库完毕"
        
        return flag  
        