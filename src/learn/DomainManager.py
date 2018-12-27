#coding=utf-8 
'''
Created on 2018年7月11日

@author: bingqiw
'''

from src.service.DomainService import DomainService
from src.service.ConceptService import ConceptService
from src.service.NLService import NLAnalysis, NLService
from src.config.Config import Config    
from BaseManager import BaseManager

class DomainManager(BaseManager):
    
#     领域新建
    REQUEST_TYPE_NEW = 0 
#     领域完善
    REQUEST_TYPE_DOMAIN = 1
    
    # 非实例化更新领域
    def refreshDomain(self, param):    
        ds = DomainService()
        domain_list = ds.refreshCognitionDomain(param)
        cs = ConceptService(param)
        cs.refreshDomainConcept(self.param,domain_list)
            
    def __isPerfectForDomain(self, domainList):
        
        domain_req = []
        isImproved = self.REQUEST_TYPE_NEW        
        for item in domainList :
            if item['tr_status'] == '0':
                domain_req.append(item)
                isImproved = self.REQUEST_TYPE_DOMAIN
#             elif item['c_tr_status'] == '0':
#                 domain_req.append(item)
#                 isImproved = self.REQUEST_TYPE_CONCEPT
                    
        if isImproved > 0:
            print "领域存在，但是需要完善..."
            
        return domain_req,isImproved
    
    def getLearnRequest(self):
        
        print "学习需求确认中 ..."
        ds = DomainService()
        #识别领域
        domainAccList,domainVagList = ds.identifyDomain(self.param)
        
        request = []
        #存在已知领域，准确找到领域定义
        if len(domainAccList)>0:
            print "精准匹配领域列表存在"
            domain_req, req_type = self.__isPerfectForDomain(domainAccList)   
            request.append({'domain_req':domain_req, 'req_type':req_type})
            
        #存在已知领域，从概念层次，找到相应领域的定义
        elif len(domainVagList)>0:
            print "模糊匹配领域列表存在"
            domain_req, req_type = self.__isPerfectForDomain(domainVagList)    
            request.append({'domain_req':domain_req, 'req_type':req_type})
        else:
            print "没有发现已知领域"    
            request.append({'req_type':self.REQUEST_TYPE_NEW})
        #不存在该领域，创建    
        if len(request)>0:
            self.param['request'] = request    
    
    def startLearn(self): 
        print "领域学习开始 ..."
        #总结学习需求
        self.getLearnRequest()
           
        param = self.param
        
        if param.has_key('request') == False:
            print "Warning request is None"
            return
        
        request = param['request']
        ds = DomainService()
        la = NLAnalysis()
        cs = ConceptService()
        
        for req in request:
            req_type = req['req_type']
            
            if req_type == self.REQUEST_TYPE_NEW:
                print "采用领域新建模式，开始 ..."
                #根据目录标题，做主题分析
                print "分析目录标题，创建主题字典，开始 ..."
                la.analyseLdaByTitle(param)
                
                print "创建主题领域，开始 ..."
                #创建领域结点
                ds.createCognitionDomain(param)
                
                #初始化概念结点
                if cs.deleteDomainConcept(param):
                    if cs.createDomainConcept(param):
                        print "创建主题领域概念，结束！"
                        #修改领域结点状态;变为生效状态
                        status = {'tr_status':'1', 'tr_id':param['tr_id']}
                        
                        dd = DomainService()
                        dd.updateDomainStatus(status)   
                        print "创建主题领域概念，结束！"
            elif req_type == self.REQUEST_TYPE_DOMAIN:
                print "采用领域完善模式，开始 ..."
                
                la.analyseLdaByTitle(param)
                print "分析目录标题，创建主题字典，结束！"
                
                param['tr_id'] = req['domain_req']['tr_id']
                ds.updateCognitionDomain(param)
                print "分析目录标题，更新主题字典，结束！"
                
                #初始化概念结点
                if cs.deleteDomainConcept(param):
                    if cs.createDomainConcept(param):
                        print "创建主题领域概念，结束！"
                        #修改领域结点状态;变为生效状态
                        status = {'tr_status':'1', 'tr_id':param['tr_id']}
                        dd = DomainService()
                        dd.updateDomainStatus(status)          
                        print "主题领域完善，结束！"

class DomainMediaManager(DomainManager):
            
    def getLearnRequest(self):
        print "获得领域学习需求，开始..."
        request = []
#         查看媒体目录需要学习的文章
        flag = NLService().getDocCatalogsForMeidaLearn(self.param)
        request.append({'isLearn':flag})
        self.param['request'] = request    
        
    def startLearn(self):
        print "开始学习 ..."
        
        self.getLearnRequest()
        
        if self.param['request'][0]['isLearn'] == False:
            print "学习需求无效 ..."
        else:
            nls = NLService()
            if nls.doMediaLearn(self.param) :
                if nls.refreshLdaDicByMedia(self.param):
                    ds = DomainService()
                    domain_list = ds.refreshCognitionDomain(self.param)
                    cs = ConceptService(self.param)
                    cs.refreshDomainConcept(self.param,domain_list)    
        
        print "学习结束！"
        
    
        
        
        