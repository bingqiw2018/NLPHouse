# -*- coding: utf-8 -*-
'''
Created on 2018年7月9日

@author: bingqiw
'''
import pandas as pd
import scrapy
from src.dao.ConceptDao import ConceptDao
from scrapy_splash import SplashRequest
import os
import threading

class SyncConceptOut(object):
    def __init__(self):
        self.lock = threading.Lock()
        
    def outConceptFile(self,concept_list, key_item):    
        self.lock.acquire()#加锁，锁住相应的资源
        
        tr_id = key_item['tr_id'] 
        tr_parent_id = key_item['tr_parent_id'] 
        
        path = 'd:/tmp/learn_concept/concept_db/concept_'+tr_id+'_'+tr_parent_id+'.cvs'
        
        df = pd.DataFrame(concept_list)    
        
        if os.path.exists(path):
            df0 = pd.read_csv(path,header=None,index_col=None)
            df = pd.concat([df0,df],ignore_index=True)
             
            if os.access(path, os.W_OK) == True:
                print "文件正常写入"+path
                df.to_csv(path,header=None,index=False)
            else:    
                print "文件不能写入，path="+path
        else:
            print "文件正常写入"+path
            df.to_csv(path,header=None,index=False)
        
        self.lock.release()#解锁，离开该资源
        return path
sc = SyncConceptOut()
    
class BaiduConceptSpider(scrapy.Spider):
    name = 'baidu_concept'
    allowed_domains = ['baike.baidu.com']
    start_urls = 'https://baike.baidu.com/item/'
    
    concept_file_path = ""
    
    # start request    
    def start_requests(self):
        ds = ConceptDao()
        #获取概念关键词
        params = {'tr_status':'0'}
        qList = ds.queryDomainConcept(params)
        
        for item in qList:
            article_url = self.start_urls+item['tr_name']
#             print "发起["+item['tr_name']+"]查询"
            yield SplashRequest(article_url, self.parse,meta={'key_item':item}, args={'wait':3}, endpoint='render.html')
    
    def parse(self, response):
        key_item = response.meta['key_item']
        concept_name = key_item['tr_name'] 
        
        qlist = response.xpath('//div[@class="lemma-summary"]/div[@class="para"]')
        print "查找概念["+concept_name+"]发现段落数："+str(len(qlist))
        
        concept_list = []
        for item in qlist:
            content = item.xpath('.//text()').extract() 
#             print " ".join(content)
            concept_list.append([concept_name," ".join(content)])
        
#         path = 'd:/tmp/learn_concept/learn_concept_'+datetime.datetime.now().strftime('%Y-%m-%d')+'.xlsx'
        
        path = sc.outConceptFile(concept_list, key_item)
        
        params = {'tr_attributes':len(concept_list),'tr_status':'1','tr_nodes':path,'tr_parent_id':key_item['tr_parent_id'],'tr_id':key_item['tr_id']}
        
        ds = ConceptDao()
        ds.finishSpideConcept(params)
