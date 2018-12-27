#coding=utf-8 
'''
Created on 2018年6月20日

@author: bingqiw
'''
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from src.service import CognitionDriverService as cognition_service
from src.service.NLService import NLAnalysis,GrammerUtil

def createDomainConcept():
#     param = {'source':'toutiao.com','keyword':u'中医按摩'}
#     lda_service.analyseByTitle(param)
    param = {'domain_name':u'中医按摩'}
    cognition_service.createDomainConcept(param)

def analyseConcept():
    list_my = ['网络红人','传统医学','中医','世界卫生组织','经络学','运动按摩','运动竞赛','中医推拿','程序员','项目经理','需求分析','系统分析师']
    
    params = {
            'user_dict':'C:/Python27/Lib/site-packages/jieba/dict_my.txt',
            'stop_words':'C:/Python27/Lib/site-packages/jieba/stopword_my.txt',
            'data_file':'d:/tmp/learn_concept/learn_concept.txt',
            'key_words':['传统医学','需求分析','系统分析师','中医推拿','经络学','中医'],
        }
    
def refreshConcept(): 
    
    params = {
            'user_dict':'C:/Python27/Lib/site-packages/jieba/dict_my.txt',
            'stop_words':'C:/Python27/Lib/site-packages/jieba/stopword_my.txt' ,
            'spider':'baidu_concept' ,
            'status':'1'                   
        }
    
if __name__ == '__main__':
    
    gUtil = GrammerUtil()
    word = "中医/中医按摩/按摩/穴位"
    str_list = word.split("/")
    
    word = "2、风池；位置：后颈部大筋两旁凹陷，与耳垂平行处。方法：食、中指一起以指腹按压，并以穴位为中心前后、左右移动。"
    gUtil.getAnalysisList(str_list, word)
    