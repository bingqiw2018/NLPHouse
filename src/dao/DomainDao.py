#coding=utf-8 
'''
Created on 2018年7月11日

@author: bingqiw
'''
from BaseDao import BaseDao

class DomainDao(BaseDao):
    
    def queryDomainForIdentify(self, param):
        
        similar_band = param['similar_band']
        sql = "select t.tr_id, t.tr_name, t.tr_nodes, t.tr_status, tc.tr_id as c_tr_id, tc.tr_name as c_tr_name, tc.tr_attributes as c_tr_attributes, tc.tr_status as c_tr_status from tr_domain t left join tr_concept tc on tc.tr_parent_id = t.tr_id "
        consult = "WHERE t.tr_status in ('1','0') "
        result = []
        
        if param and len(param)>0:
            arr = []
            
            if 'domain_name' in param.keys() :
                arr.append(param['domain_name'])
                if similar_band == '1':
                    consult += "and t.tr_name = %s "
                elif similar_band == '2':
                    consult += "and locate(%s,t.tr_nodes) > 0 "
                    
            sql += consult    
            result = self.db.select(sql, arr)
        else:
            print 'param is none, service quit !!!'        
                
        return result
    
    def queryDomainForConcept(self, param):   
        sql = "SELECT tr_id, tr_name, tr_nodes, create_time FROM tr_domain "
        consult = "WHERE tr_status = '0' "
        result = []
        if param and len(param)>0:
            arr = []
            
            if 'domain_name' in param.keys() :
                arr.append(param['domain_name'])
#                 consult += "and locate(%s,tr_nodes) > 0 "
                consult += "and tr_name=%s "
            
            sql += consult    
            result = self.db.select(sql, arr)
        else:
            print 'param is none, service quit !!!'    
        
        return result
    
    # 创建认知树领域层结点
    def createCognitionDomain(self, param):  
        sql = "insert tr_domain (tr_id, tr_name, tr_nodes, create_time) VALUES (%s, %s, %s, %s)"
        arr = []
        arr.append([param['tr_id'],param['domain_name'],param['domain_concept'],param['create_time']])
        
        flag = self.db.batch_sql(sql,arr)
        print "入库完毕"
        return flag    
    
    def updateDomainStatus(self, status):
        sql = "update tr_domain set tr_status=%s where tr_id=%s "
        arr = []
        
        arr.append([status['tr_status'],status['tr_id']])
        
        flag = self.db.batch_sql(sql,arr)
        print "修改完毕"
        return flag
    
    def updateCognitionDomain(self, param ):
        sql = "update tr_domain set tr_nodes=%s, tr_status='0' where tr_id=%s "
        arr = []
        
        arr.append([param['domain_concept'],param['tr_id']])
        
        flag = self.db.batch_sql(sql,arr)
        print "修改完毕"
        return flag

    def refreshCognitionDomain(self, param ):
        sql = "update tr_domain set tr_nodes=%s where tr_id=%s "
        arr = []
        
        arr.append([param['domain_concept'],param['tr_id']])
        
        flag = self.db.batch_sql(sql,arr)
        print "修改完毕"
        return flag
    
    def queryDomainForRefresh(self, param):
        
        sql = "SELECT tr_id, tr_name, tr_nodes FROM tr_domain "
        consult = "WHERE tr_status in ('0','1') "
        
        arr = []
        sql += consult    
        result = self.db.select(sql, arr)
        
        return result
        
        
        
        