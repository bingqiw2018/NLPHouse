#coding=utf-8 
'''
Created on 2018年6月20日

@author: bingqiw
'''
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from src.learn.CognitionDriver import CognitionDriver        
if __name__ == '__main__':
    cd = CognitionDriver()
    cd.learnCognitionByGuide({'guide_learn_type':'passage'})
#     param = {'domain_name':'中医按摩'}
#     cd.searchCognitionBySelf(param)
    
