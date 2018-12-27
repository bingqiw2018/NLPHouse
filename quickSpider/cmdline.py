#coding=utf-8 
'''
Created on 2018年6月2日

@author: bingqiw
'''
import scrapy.cmdline  
  
if __name__ == '__main__':  
    
    scrapy.cmdline.execute(argv=['scrapy','crawl','baidu_concept'])  
