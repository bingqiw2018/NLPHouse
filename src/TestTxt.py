#coding=utf-8 
'''
Created on 2018年7月4日

@author: bingqiw
'''
import pandas as pd

data = pd.read_table('d:/tmp/learn_concept/learn_concept.txt',header=None,encoding='utf-8')
print('数据录入完毕')
print(data.shape)