# -*- coding: utf-8 -*-
'''
Created on 2018年7月14日

@author: bingqiw
'''
import json
from scrapy_splash import SplashRequest
from src.service.SpiderService import SpiderService 
from src.utils import DateUtils as du
import scrapy

class ToutiaoSearchSpider(scrapy.Spider):
    name = 'toutiao_search'
    allowed_domains = ['www.toutiao.com']
    
    start_urls = 'https://www.toutiao.com/search_content/?offset={num}&format=json&keyword={keywords}&autoload=true&count=20&cur_tab=1&from=search_tab'
#   采集关键字
    keywords = []
    
    #   是否进行抓取数据
    flag = True
    
#   采集步长
    step = 20
    
    def start_requests(self):
        
        param = {'spider_id':self.name}
        
        ss = SpiderService(param)
        self.keywords = ss.querySessionKeywords(param)
        
        count = 0
        
        if len(self.keywords) == 1:
            print "发现会话语句："+self.keywords[0]['words']
            self.start_urls = self.start_urls.replace('{keywords}', self.keywords[0]['words'])
            
            while self.flag:
                url = self.start_urls.replace('{num}', str(count))
                count += self.step
                yield SplashRequest(url, self.parse, args={'wait': 3}, endpoint='render.html')
                
        else:
            print "没有发现会话语句"
    
    
    def parse(self, response):    
           
        result_list = response.xpath('//pre/text()').extract_first()
        arr = json.loads(result_list)['data']
        
        source = "toutiao.com"
        doc_list = []
        for item in arr:
            toutiao_item = {}
            toutiao_item['doc_id'] = du.get_unit_id()
            toutiao_item['doc_type'] = "1" #文章类型：1=文章；2=视频',
            toutiao_item['sp_type'] = "1" #抓取类型：1=搜索；2=媒体',
            toutiao_item['abstract'] = item.get('abstract')
            toutiao_item['article_url'] = item.get('article_url')
            toutiao_item['comment_count'] = item.get('comment_count')
            toutiao_item['datetime'] = item.get('datetime')
            toutiao_item['create_time'] = du.current_time()
            toutiao_item['image_url'] = item.get('image_url')
            toutiao_item['keyword'] = item.get('keyword')
            toutiao_item['media_name'] = item.get('media_name')
            toutiao_item['source'] = source
            toutiao_item['tag'] = item.get('tag')
            toutiao_item['tag_id'] = item.get('tag_id')
            toutiao_item['title'] = item.get('title')
            toutiao_item['video_duration'] = item.get('video_duration')
            if self.check_doc(toutiao_item):
                doc_list.append(toutiao_item)  
#                 print('{}、{},{}'.format(item['doc_id'],item['title'],item['doc_id'])) 
                
        if len(doc_list) == 0:
            self.flag = False
#             print "没有发现文章可以被抓取"
        else:
            ss = SpiderService()
            print "搜索内容准备入库 ..."
            ss.getDocCatalogs(doc_list)    
             
    def check_doc(self,item):
        
        if item['video_duration'] != None:
            return False
        
        if item['title'] == None:
            return False
        
        if item['article_url'] == None:
            return False
        
        return True