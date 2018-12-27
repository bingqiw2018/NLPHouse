#coding=utf-8 
'''
Created on 2018年4月24日

@author: bingqiw
'''
import MySQLdb as md
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf8') 

class DataSource(object):

    doc_db_con =  md.connect(host='127.0.0.1', port=3306,user='root', passwd='123456', db='doc_db', charset='utf8')

class DBManager(DataSource):

    __con = None
    def __init__(self):
        self.__con = self.doc_db_con
        
    def qry_sql(self, sql):
        df = pd.read_sql(sql, con=self.__con) 
        print "Execute:"+sql
        return df
    
    def select(self, sql, param):
        
        cur = self.__con.cursor(cursorclass = md.cursors.DictCursor)
        print sql
        self.__printParam(param)
        reCout = cur.execute(sql, param)
        print('data done size:{}'.format(reCout)) 
        arr = cur.fetchall()
        result = []
        for i in arr:
            result.append(i)
            
        self.__con.commit()
        cur.close()
        return result
    
    def execute(self, sql, param):
        cur = self.__con.cursor()
        print sql
        self.__printParam(param)
        reCout = cur.execute(sql, param)
        print('data done size:{}'.format(reCout)) 
        self.__con.commit()
        cur.close()
        return reCout
    
    def batch_sql(self, sql, param_list):    
        cur = self.__con.cursor()
        print "sql=",sql
#         self.__printParamList(param_list)
        print param_list    
        reCout = cur.executemany(sql, param_list)
        print('data done size:{}'.format(reCout)) 
        self.__con.commit()
        cur.close()
        return reCout
    
    def __printParam(self, param):
        item_list = []
        for item in param:
            item_list.append(str(item))
        print '['+','.join(item_list)+']'
        
    def __printParamList(self, param_list):
        
        for param in param_list:
            item_str = ",".join( str(item) for item in param    )
            print '['+item_str+']'
            