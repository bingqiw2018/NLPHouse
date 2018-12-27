#coding=utf-8 
'''
Created on 2018年7月11日

@author: bingqiw
'''

from src.dao.DomainDao import DomainDao
from src.dao.NLDao import NLDao
from src.utils import DateUtils as du
from BaseService import BaseService

class DomainService(BaseService):
    
#     无条件更新领域信息
    DOMAIN_REQUEST_REFRESH = 1
    
#     条件更新
    DOMAIN_REQUEST_CONDITION = 0
    
    def initParam(self, params={}, dao=None):
        BaseService.initParam(self, params, DomainDao())
        
#     识别领域
    def identifyDomain(self, params):
        domain_name = params['domain_name']
        similar_band = '1' # '1'= 精准匹配；'2'=模糊匹配
        param = {'domain_name':domain_name, 'similar_band':similar_band}
        dd = DomainDao()
        list_acc = dd.queryDomainForIdentify(param)
        
        similar_band = '2'
        param = {'domain_name':domain_name, 'similar_band':similar_band}
        list_vag = dd.queryDomainForIdentify(param)
        
        return list_acc, list_vag
        
    # 定义认知领域
    def createCognitionDomain(self, param):
        
        domain_name = param['domain_name']
        create_time = du.current_time()
        domain_concept = self.__getDomainConceptByDic(domain_name)
        tr_id =  du.get_unit_id()
        
        param['tr_id'] = tr_id
        
        params = {'tr_id':tr_id, 'domain_name':domain_name,'create_time':create_time, 'domain_concept':domain_concept}
        self.dao.createCognitionDomain(params)
        
    # 获得领域层概念，通过给定的领域名称，对高频词典词汇进行过滤        
    def __getDomainConceptByDic(self, domain_name):
    
        param = {'domain_name':domain_name}
        
        ds = NLDao()   
        result = ds.getDomainConceptByDic(param)    
        result = ",".join( item['dic_word'] for item in result)
        
        return result 
    
    # 更新认知领域，用于领域创建过程
    def updateCognitionDomain(self, param):   
        domain_name = param['domain_name']
        tr_id = param['tr_id'] 
        
        domain_concept = self.__getDomainConceptByDic(domain_name)
        param = {'tr_id':tr_id, 'domain_concept':domain_concept}
        
        return self.dao.updateCognitionDomain(param)
    
    # 用于对语料库的优化功能
    def refreshCognitionDomain(self,param):
        print "更新领域..."
        domain_list = self.dao.queryDomainForRefresh(param)
        
        result_list = []
        for domain in domain_list:
            d_name = domain['tr_name']
            d_id = domain['tr_id']    
            param = {'domain_name':d_name, 'tr_id':d_id}
            count = self.updateCognitionDomain(param)
            if count > 0:
                result_list.append(domain)
        print "成功更新领域："  + str(len(result_list) )   
        print "更新领域结束！"  
        return result_list
    
    def updateDomainStatus(self,status):    
        self.dao.updateDomainStatus(status)