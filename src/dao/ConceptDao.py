#coding=utf-8 
'''
Created on 2018年7月11日

@author: bingqiw
'''
from BaseDao import BaseDao

class ConceptDao(BaseDao):
    
    # 创建概念层结点
    def createDomainConcept(self, param_list):
        sql = "insert tr_concept (tr_id, tr_parent_id, tr_name, create_time) VALUES (%s, %s, %s, %s)"
        arr = []
        
        for param in param_list:
            arr.append([param['tr_id'],param['tr_parent_id'],param['tr_name'],param['create_time']])
        
        flag = self.db.batch_sql(sql,arr)
        print "入库完毕"
        return flag     
    
    def queryDomainConcept(self, param):   
        sql = "SELECT tr_id, tr_parent_id,  tr_name, tr_attributes FROM tr_concept "
        consult = "WHERE  "
        result = []
        
        if param and len(param)>0:
            arr = []
            
            if 'tr_status' in param.keys() :
                arr.append(param['tr_status'])
                consult += "tr_status = %s  "
            
            sql += consult    
            result = self.db.select( sql, arr)
        else:
            print 'param is none, service quit !!!'  
        
        return result 
    
    def refreshDomainConcept(self, param_list):
        sql = "update tr_concept set tr_status=%s where tr_id=%s and tr_parent_id= %s"
        arr = []
        
        for param in param_list:
            arr.append([param['tr_status'], param['tr_id'],param['tr_parent_id']])
        
        flag = self.db.batch_sql(sql,arr)
        print "修改完毕"
        return flag
    
    def finishSpideConcept(self, params):
        sql = "update tr_concept set tr_status=%s, tr_nodes=%s , tr_attributes=%s where tr_id=%s and tr_parent_id= %s"
        arr = []
        
        arr.append([params['tr_status'], params['tr_nodes'], params['tr_attributes'], params['tr_id'],params['tr_parent_id']])
        
        flag = self.db.batch_sql(sql,arr)
        print "修改完毕"
        return flag
    
    def deleteDomainConcept(self, params):
        sql = "delete from tr_concept where tr_parent_id= %s"
        arr = []
        
        arr.append([params['tr_id']])
        
        flag = self.db.batch_sql(sql,arr)
        print "修改完毕"
        return flag