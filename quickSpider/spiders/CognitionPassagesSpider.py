# -*- coding: utf-8 -*-
'''
Created on 2018年7月30日

@author: bingqiw
'''
from scrapy_splash import SplashRequest
from src.service.SpiderService import SpiderService
from src.utils import DateUtils as du
import scrapy

class ToutiaoPassagesSpider(scrapy.Spider):
    
    name = 'toutiao_passages'
    
    start_urls = []
    
    script = '''
        function main(splash, args)
          splash:set_viewport_size(1028,500) 
          splash.scroll_to(0,1000)
          assert(splash:go(args.url))  
          assert(splash:wait(0.5))
          return {
            html = splash:html(),
            png = splash:png(),
            har = splash:har(),
          }
        end
    '''
    # start request    
    def start_requests(self):
        
        param = {}
        
        ss = SpiderService()
        data = ss.queryDocCatalogsWithoutPassages(param)
        
        params = []
        
        for item in data:
#             print item['title'],item['article_url']
            article_url = ''
            doc_id = item['doc_id']
            media_id = item['media_id']
            source = item['source']
            
            if 'http://toutiao.com/group/' in item['article_url']:
                article_url = item['article_url'].replace('http://toutiao.com/group/','http://toutiao.com/a')
            if '/item/' in item['article_url']:
                article_url = item['article_url'].replace('http://toutiao.com','').replace('/item/','http://toutiao.com/i')
            else:
                article_url = item['article_url']   
            params.append({'doc_id':doc_id, 'article_url':article_url, 'media_id':media_id, 'source':source})  
              
#         print '待处理的urls:',len(urls)              
        for param in params:
            article_url = param['article_url']
            doc_id = param['doc_id']
            media_id = param['media_id']
            source = param['source']
            yield SplashRequest(article_url, self.parse,meta={'doc_id':doc_id, 'media_id':media_id, 'source':source}, args={'wait':3}, endpoint='render.html')
    
    # parse the html content 
    def parse(self, response):
        
        arr = self.parsePsgCnt(response,'0')# 0=解析段落；1=解析关键字
        keyword = self.parsePsgCnt(response,'1')# 0=解析段落；1=解析关键字
        keyword = ','.join(keyword)
        
        param = []
        doc_id = response.meta['doc_id'] 
        count = 0
        for pa in arr:
            pa = pa[0:5000]
            param.append({
                'psg_id': du.get_unit_id(),
                'doc_id': doc_id,
                'psg_id': du.get_unit_id(),
                'psg_order': count,
                'psg_content': pa,
                'create_time': du.current_time(),
                'psg_keywords': keyword
                })
            count += 1 
         
        if len(param) > 0 :   
            ss = SpiderService()
            ss.getDocPassages(param)
        else:
            print('解析结果异常：doc_id={}'.format(doc_id))