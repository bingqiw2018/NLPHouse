# -*- coding: utf-8 -*-
'''
Created on 2018年7月15日

@author: bingqiw
'''
from scrapy_splash import SplashRequest
from src.service.SpiderService import SpiderService

from src.utils import DateUtils as du
import re
import scrapy

class ToutiaoMediaSpider(scrapy.Spider):

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
    isToday = False
    
    # parse the html content 
    def parse(self, response):
        
        qlist = response.xpath('//div[@class="relatedFeed"]/ul/li/div')
        media_name = response.xpath('//div[@class="yheader"]/div/ul/li/a/span[1]//text()').extract_first()
        
        media_id=response.meta['media_id']  
        
        doc_list = []
        for item in qlist:
            title = item.css('div.title-box').xpath('./a/text()').extract_first()
            article_url = item.css('div.title-box').xpath('./a/@href').extract_first()
            view_num = item.css('div.y-left').xpath('./a[1]/text()').extract_first() 
            comment_count = item.css('div.y-left').xpath('./a[2]/text()').extract_first() 
            date_time = item.css('div.y-left').xpath('./span//text()').extract() 
            img_url = item.css('div.lbox').xpath('./a/img/@src').extract_first()
             
            if len(date_time) == 2:
                date_time = date_time[1]
            else:
                date_time = date_time[0]    
                
            date_time = date_time.replace('⋅ ','')
            curr_time = du.current_time()
            
            if self.isToday and du.is_current_fdate(date_time, '%Y-%m-%d %H:%M') == False:
                continue
            
            toutiaoItem = {}
            toutiaoItem['doc_id'] = du.get_unit_id()
            toutiaoItem['doc_type'] = "1"
            toutiaoItem['sp_type'] = "2"
            toutiaoItem['datetime'] = date_time
            toutiaoItem['create_time'] = curr_time
            toutiaoItem['image_url'] = img_url
            toutiaoItem['media_name'] = media_name
            toutiaoItem['media_id'] = media_id
            toutiaoItem['source'] = "toutiao.com"
            toutiaoItem['title'] = title
            
            if float(comment_count.replace('评论','').replace(' ','')) > 0 :
                toutiaoItem['comment_count'] = float(comment_count.replace('评论','').replace(' ',''))
            else:
                toutiaoItem['comment_count'] = '0.0'  
            
            
            if '播放' in view_num:
                continue
            
            f_view_num = float(re.sub('[^\d.]', '', view_num))
            
            if f_view_num > 0 :     
                if '万' in view_num:
                    toutiaoItem['view_num'] = f_view_num*10000
                else:
                    toutiaoItem['view_num'] = f_view_num
            else:
                toutiaoItem['view_num'] = '0.0'  
                
            toutiaoItem['article_url'] = article_url
            doc_list.append(toutiaoItem)  
        
        if len(doc_list) > 0:
            SpiderService().getMediaCatalogs(doc_list)  

class ToutiaoMediaOnlySpider(ToutiaoMediaSpider):
    
    name = 'toutiao_media_only'

    # start request    
    def start_requests(self):
        
        param = {'source':'toutiao.com', 'media_id':''}
        ss = SpiderService()
        media_list = ss.queryToutiaoMediaUser(param)#对当前的数据进行加载
        
        for media in media_list:
                yield SplashRequest(media['user_url'], self.parse, meta={'media_id':media['media_id']}, args={'lua_source': self.script, 'wait': 0.5, 'images':0}, endpoint='execute')
          
     

class ToutiaoMediaTodaySpider(ToutiaoMediaSpider):
    
    name = 'toutiao_media_today'

    # start request    
    def start_requests(self):
        param = {'source':'toutiao.com'}
        ss = SpiderService()
        
        self.isToday = True
        
        media_list = ss.queryToutiaoMediaUser(param)#对当前的数据进行加载
        
        for media in media_list:
                yield SplashRequest(media['user_url'], self.parse, meta={'media_id':media['media_id']}, args={'lua_source': self.script, 'wait': 0.5, 'images':0}, endpoint='execute')
          
              
class ToutiaoMediaUnlearnSpider(ToutiaoMediaSpider):
    
    name = 'toutiao_media_unlearn'
    
    # start request    
    def start_requests(self):
        
        param = {'source':'toutiao.com'}
        ss = SpiderService()
#         if self.isMediaUrl == True:
#             for url in self.start_urls:
#                 yield SplashRequest(url, self.parse, meta={'media_id':param['media_id']}, args={'lua_source': self.script, 'wait': 0.5, 'images':0}, endpoint='execute')
#         else:
#             if self.isToday == False:#对没有加载文章目录的媒体进行数据加载
#                 media_list = ds.queryToutiaoMediaUserUnDone(param)
#             else:
#                 media_list = ds.queryToutiaoMediaUser(param)#对当前的数据进行加载
#                 
#             for media in media_list:
#                 yield SplashRequest(media['user_url'], self.parse, meta={'media_id':media['media_id']}, args={'lua_source': self.script, 'wait': 0.5, 'images':0}, endpoint='execute')
        media_list = ss.queryToutiaoMediaUserUnDone(param)         
        
        for media in media_list:
                yield SplashRequest(media['user_url'], self.parse, meta={'media_id':media['media_id']}, args={'lua_source': self.script, 'wait': 0.5, 'images':0}, endpoint='execute')
                
        