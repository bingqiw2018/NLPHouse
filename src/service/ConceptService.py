#coding=utf-8 
'''
Created on 2018年7月11日

@author: bingqiw
'''
import pandas as pd
import jieba.posseg as jp
import jieba
import jieba.analyse as ja
import os

from src.dao.DomainDao import DomainDao
from src.dao.ConceptDao import ConceptDao 
from src.utils import DateUtils as du

from BaseService import BaseService

class ConceptService(BaseService):
    
    __learn_data = None
    __keywords = None
    __spider = None
    __status = None
    
    def initParam(self, params={}, dao=None):
        BaseService.initParam(self, params, ConceptDao())
        
    def __suggestFreq(self, item):
        
        concept_name = item['tr_name']
        
        self.__keywords = []
        
        self.__keywords.append(concept_name)
        
        for keyword in self.__keywords:
            jieba.suggest_freq(keyword, True)
    
    def __extractContent(self, item):
        data_source = item['tr_attributes']
        print '读入数据源：'+str(data_source)
        
        texts = []
        try:
            self.__learn_data = pd.read_csv(data_source,header=None,index_col=None,encoding='utf-8')
            
            for index in range(len(self.__learn_data)):
                cause = self.__learn_data.loc[index, 1]
                texts.append(cause)
        
        except BaseException as ex:
            print('except:', ex)
            
        return texts  
                
    def __findConcept(self, item):
        #上调词频
        self.__suggestFreq(item)
        
        #抽取内容，概念词在句首的句子
        texts = self.__extractContent(item)
        
        #判断非主语的句子部分词性
        exits_concept = self.__checkConcept(item, texts)
            
        return exits_concept    
    
    def __checkConcept(self, item, texts):    
        
        concept_name = item['tr_name']
        data_source = item['tr_attributes']
        
        exits_concept = 0
        str_buffer = []
        text_buffer = []
        concept_num = 0
        for text in texts:
            
            text_file = [concept_name,text,0]
            text = text.replace('“'+concept_name+'”',concept_name,1)
            text = text.replace('"'+concept_name+'"',concept_name,1)

            if text.find(concept_name) < 0:
                text_buffer.append(text_file)
                continue
                
            flag_c = text.find(concept_name)
            if flag_c == 0:   #关键字在句首
                sub_text = text.replace(concept_name,'',1)
    #             words = jp.cut(sub_text)
    #             print ("/".join(word+flag for word, flag in words) )
    
                flag_c = sub_text.find('是')
                if flag_c > -1: #存在判定关键字“是”
                    
                    #结构分析
                    clauses = sub_text.split("。")
                    
                    for clause in clauses:
                        clause_p = clause+"。"
                        d_clauses = clause_p.split("，")
                        
                        for d_clause in d_clauses:
                            
                            if d_clause.find('的')>-1:
                                
                                sub_clauses = d_clause.split('的')
                                last_sub_clause = sub_clauses[len(sub_clauses)-1].replace('。','')
                                
                                #词性分析
                                last_words = jp.cut(last_sub_clause)
                                for word, flag in last_words:
                                    possegs = ['n','l']
                                    for pos_w in possegs:
                                        if flag.find(pos_w)>-1:
                                            if clause_p.find(word+"，") > -1 or clause_p.find(word+"。") > -1:
                                                concept_str = concept_name+"="+last_sub_clause
                                                str_buffer.append(concept_str)
                                                text_file = [concept_name,text,1]
                                                concept_num += 1
            
            text_buffer.append(text_file)
                                                
        if concept_num == 0:
            print "["+concept_name+"]没有发现概念定义，文件："+data_source
            exits_concept = 0
        else:
            
            if concept_num >= len(texts):
                exits_concept = 1
            else:
                exits_concept = 2
                
            df = pd.DataFrame(text_buffer)    
            df.to_csv(data_source,header=None,index=False)
            print "["+concept_name+"]"+"/".join(str_buffer)
            
        return exits_concept 
    
#     创建领域概念结点内容       
    def refreshConcept(self):
        
        try:
            print "概念数据抓取..."
#             scrapy.cmdline.execute(argv=['scrapy','crawl',self.__spider['concept_spider']])  
            os.system("scrapy crawl "+self.param['spider']['concept_spider'])
            print "概念数据抓取，结束！"
        finally:
            flag = True
            count = 1
            while(flag == True):
                print "概念检查程序，第("+str(count)+")次，开始执行..."
                
                params = {'tr_status':self.param['status']}
                qList = self.dao.queryDomainConcept(params)
                
                if len(qList) == 0:
                    print "概念检查程序执行完毕！"
                    flag = False
                    break
                
                param_list = []                
                for item in qList:

                    isConcept = self.__findConcept(item)
                    
                    if isConcept == 0:
                        param = {'tr_id':item['tr_id'], 'tr_parent_id':item['tr_parent_id'], 'tr_status':'2'}
                        param_list.append(param)
                    elif isConcept == 1:
                        param = {'tr_id':item['tr_id'], 'tr_parent_id':item['tr_parent_id'], 'tr_status':'3'}
                        param_list.append(param)
                    elif isConcept == 2:
                        param = {'tr_id':item['tr_id'], 'tr_parent_id':item['tr_parent_id'], 'tr_status':'4'}
                        param_list.append(param)
                        
                self.dao.refreshDomainConcept(param_list)
                
                count+=1
    
    def refreshDomainConcept(self, param, domain_list):
        
        print "更新概念，初始化领域概念开始..."
        for domain in domain_list:
            
            param['domain_name'] = domain['tr_name']
            param['domain_name'] = domain['tr_id']  
            if self.deleteDomainConcept(param):
                return self.createDomainConcept(param)
            
        self.refreshConcept()    
        print "更新概念，初始化领域概念，结束！！"
             
    #   删除领域概念          
    def deleteDomainConcept(self, param):    
        
        flag = True
        try:   
            self.dao.deleteDomainConcept(param)
        except BaseException as ex:
            print('except:', ex)
            flag = False
        return flag
                        
    # 建立领域的概念结点，可以根据领域名称对某一个领域建立概念结点
    def createDomainConcept(self, param):
        
        dd = DomainDao()
        concept_list = dd.queryDomainForConcept(param)
        
        flag = True
        for item in concept_list:
            words = item['tr_nodes'].split(',')
            
            param_list = self.__getConceptParam(item,words)
            
            #概念入库    
            try:
                self.dao.createDomainConcept(param_list)
            except BaseException as ex:
                print('except:', ex)
                flag = False
                
        return flag
    
    # 解析概念关键字        
    def __getConceptParam(self, item, words):
        
        param_list = []
        
        for word in words:
            tr_parent_id = item['tr_id']
            tr_id = du.get_unit_id()
            create_time = du.current_time()
            tr_name = word
            
            param = {'tr_id':tr_id, 'tr_parent_id':tr_parent_id, 'tr_name':tr_name, 'create_time':create_time}  
            param_list.append(param)
        
        return param_list