#coding=utf-8 
'''
Created on 2018年7月25日

@author: bingqiw
'''
class Config(object):
    
    __param = None
    
    def __init__(self):
        
        self.__param = {
            'source':'toutiao.com',
            'loc_file_path':{'loc_passage_path':'d:/tmp/learn_concept/passage_db/'},
            'spider':{'concept_spider':'baidu_concept', 
                      'media_unlearn_spider':'toutiao_media_unlearn',
                      'media_only_spider':'toutiao_media_only',
                      'media_today_spider':'toutiao_media_today',
                      'search_spider':'toutiao_search'},
            'user_dict':'C:/Python27/Lib/site-packages/jieba/dict_my.txt',
            'stop_words':'C:/Python27/Lib/site-packages/jieba/stopword_my.txt' ,
            'status':'1'  #更新概念的状态
        }
        
    def getConfigParam(self): 
        return self.__param   