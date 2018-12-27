#coding=utf-8 
'''
Created on 2018年8月6日

@author: bingqiw
'''
from BaseDao import BaseDao

class PassageDao(BaseDao):
    
    def queryConceptForPsg(self, param):
        sql = "select t.tr_id, t.tr_name, d.tr_name as domain_keyword , p.tr_id from tr_concept t left join tr_domain d on d.tr_id = t.tr_parent_id left join tr_passage p on p.tr_parent_id = t.tr_id where p.tr_id is null"
        result = self.db.select( sql, [])
        return result 
    
    
    def createCognitionPassages(self, param_list):
        sql = "insert tr_passage (tr_id, tr_parent_id, tr_name, create_time) VALUES (%s, %s, %s, %s)"
        arr = []
        
        for param in param_list:
            arr.append([param['tr_id'],param['tr_parent_id'],param['tr_name'],param['create_time']])
        
        count = self.db.batch_sql(sql,arr)
        print "入库完毕"
        return count     
    
    def updateCognitionPsg(self, param):
        
        sql = "update tr_passage set tr_attributes=%s, tr_nodes=%s, tr_status='1' where tr_id=%s and tr_parent_id=%s"
        arr = []
        
        arr.append([param['psg_num'], param['psg_path'],param['tr_psg_id'],param['tr_psg_parent_id']])
        
        count = self.db.batch_sql(sql,arr)
        print "操作完毕"
        return count     
        
        