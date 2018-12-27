#coding=utf-8 
'''
Created on 2018年7月11日

@author: bingqiw
'''
from BaseDao import BaseDao
from src.utils import DateUtils as du

class NLDao(BaseDao):
    
    def queryTitleDoc(self, param):
        sql = "select t.title from sp_doc_catalogs t limit 50"
    
        arr = []        
        nl_doc_cata_list = self.db.select( sql, arr)
        
        return nl_doc_cata_list
    
    def refreshLdaDic(self, key, data_list):
        sql = "delete from nl_dic_words where word_group = %s"
        
        arr = []  
        arr.append(key)
        
        self.db.execute( sql, arr)
        
        self.importLdaDic(data_list)
    
    def queryLdaDicByMedia(self, param):
        sql = "select t.doc_id, t.keywords, t.domain_id, t.domain_keyword from nl_doc_catalogs t where t.domain_id is not null"
        
        arr = []        
        nl_doc_cata_list = self.db.select( sql, arr)
        
        sql = "select t.dic_id, t.word_group, t.dic_word from nl_dic_words t left join nl_doc_catalogs c on c.domain_keyword = t.word_group where c.domain_id is not null"
        nl_dic_word_list = self.db.select( sql, arr)
        
        return nl_doc_cata_list, nl_dic_word_list
    
    def queryDocPsgByConcept(self, param):
        
        sql = "select t.psg_id, t.doc_id, t.psg_content, t.dic_keywords, t.psg_keywords from nl_doc_passages t where instr(t.domain_keywords,%s)>0 and instr(t.dic_keywords,%s)>0 "
        
        arr = []        
        arr.append(param['domain_keyword'])
        arr.append(param['tr_name'])
        q_list = self.db.select( sql, arr)
        return q_list
        
    def updateDocPsgForPsgLearn(self, param_list):    
        sql = "update nl_doc_passages set dic_keywords=%s, psg_keywords=%s, similar_ratio=%s, similar_limit=%s, domain_keywords=%s where doc_id = %s and psg_id = %s"
        
        arr = []
        for doc in param_list:
            arr.append([doc['dic_keywords'],doc['psg_keywords'],doc['similar_ratio'],doc['similar_limit'],doc['domain_keyword'],doc['doc_id'],doc['psg_id']])
        
        flag = self.db.batch_sql(sql,arr)
        
        return flag     
        
    def updateDocCatalogsForMeidaLearn(self, param_list):
        sql = "update nl_doc_catalogs set keywords=%s, similar_ratio=%s, similar_limit=%s, domain_id=%s, domain_keyword=%s where doc_id = %s"
        
        arr = []
        for doc in param_list:
            arr.append([doc['keywords'],doc['similar_ratio'],doc['similar_limit'],doc['domain_id'],doc['domain_keyword'],doc['doc_id']])
        
        flag = -1
        
        try:
            flag = self.db.batch_sql(sql,arr)
            print "入库完毕"
        except (BaseException),e:
            print "入库异常："+str(e)
        
        return flag     
    
    def queryDocPsgForPsgLearn(self, param):    
        sql = "select t.doc_id, t.psg_id, t.psg_content, t.dic_keywords from nl_doc_passages t where t.dic_keywords is null"
        
        arr = []        
        result = self.db.select( sql, arr)
        
        return result
    
    def queryDocCatalogsForMeidaLearn(self, param):
        
        sql = "select t.doc_id, c.title, c.abstract from nl_doc_catalogs t left join sp_doc_catalogs c on c.doc_id = t.doc_id where t.domain_id is null and c.title is not null"
        
        arr = []        
        result = self.db.select( sql, arr)
        
        return result
    
    def getDocPsgForPsgLearn(self , param):
        sql = "insert nl_doc_passages(doc_id, psg_id, psg_content, create_time) select t.doc_id, t.psg_id, t.psg_content, %s from sp_doc_passages t left join nl_doc_passages n on n.doc_id = t.doc_id and n.psg_id = t.psg_id "
        cond = "where n.doc_id is null limit 500"
        
        count = 0
        if param and len(param)>0:
            arr = []
            arr.append(du.current_time())
            sql += cond
            count = self.db.execute( sql, arr)
        else:
            print 'param is none, service quit !!!'    
        
        return count
    
    def getDocCatalogsForMeidaLearn(self, param):
        sql = "insert nl_doc_catalogs (doc_id, create_time) select t.doc_id, %s from sp_doc_catalogs t"
        cond = " where t.sp_type = '2' and t.doc_id not in (select doc_id from nl_doc_catalogs )"
        
        count = 0
        if param and len(param)>0:
            arr = []
            
            arr.append(du.current_time())
            
            isCond = False
            
            if 'source' in param.keys() :
                arr.append(param['source'])
                cond += " and t.source=%s "
                isCond = True
                
            if isCond :
                sql += cond
            
            count = self.db.execute( sql, arr)
        else:
            print 'param is none, service quit !!!'    
        
        return count
    
    # 查询文章目录
    # param为字典类型数据
    def queryDocCatalogs(self, param):
        sql = "select t.doc_id, t.source, t.doc_type, t.sp_type, t.title, t.abstract, t.article_url, t.image_url, t.comment_count, t.datetime, t.create_time, t.keyword, t.media_name, t.tag, t.tag_id from sp_doc_catalogs t"
        cond = " where 1=1 "
        
        result = []
        if param and len(param)>0:
            arr = []
            
            isCond = False
            
            if 'source' in param.keys() :
                arr.append(param['source'])
                cond += " and t.source=%s "
                isCond = True
                
            if 'domain_name' in param.keys() :
                arr.append(param['domain_name'])
                cond += " and t.keyword=%s "
                isCond = True
                    
            if 'create_time' in param.keys():
                arr.append(param['create_time'])
                cond += " and date_format(t.create_time,'"+param['format']+"')=%s "
                isCond = True
            
            if 'doc_id' in param.keys() :
                arr.append(param['doc_id'])
                cond += " and t.doc_id=%s "
                isCond = True
                
            if isCond :
                sql += cond
            
            result = self.db.select( sql, arr)
        else:
            print 'param is none, service quit !!!'    
        
        return result
    
    # 获得领域层概念，通过给定的领域名称，对高频词典词汇进行过滤
    def getDomainConceptByDic(self, param):   
        sql = "SELECT T.dic_id, t.word_group, t.dic_word, t.word_freq, t.create_time FROM NL_DIC_WORDS T WHERE T.word_group = %s  ORDER BY T.WORD_FREQ DESC LIMIT 4"
        
        result = []
        if param and len(param)>0:
            arr = []
            
            if 'domain_name' in param.keys() :
                arr.append(param['domain_name'])
            
            result = self.db.select( sql, arr)
        else:
            print 'param is none, service quit !!!'    
        
        return result
    
    def queryLdaDic(self, param):
        sql = "select t.word_group, d.tr_id from (select t.word_group from nl_dic_words t group by t.word_group) t left join tr_domain d on d.tr_name = t.word_group"
        arr = self.db.select( sql, [])
        print "字典领域分组规模："+str(len(arr))
        word_group = {}
        
        for index in range(len(arr)):
            word_group[arr[index]['word_group']] = {'tr_id':arr[index]['tr_id'], 'tr_list':[]}
        
        s_sql = "select t.word_group, t.dic_word from nl_dic_words t"
        q_list = self.db.select(s_sql,[])
        print "主题字典规模："+str(len(q_list))
        result = []
        for item in q_list:
            group = word_group[item['word_group']]['tr_list']
            group.append(item['dic_word'])
        
        for key in word_group:    
            result.append({'key':key, 'value':word_group[key]['tr_list'], 'tr_id':word_group[key]['tr_id']})
            
        return result
    
    def importLdaDic(self, doc_list):
        
        sql = "insert nl_dic_words (dic_id, word_group, dic_word, word_freq, create_time) VALUES (%s, %s, %s, %s, %s)"
        arr = []
        for doc in doc_list:
            arr.append([doc['dic_id'],doc['word_group'],doc['dic_word'],doc['word_freq'],doc['create_time']])
        
        flag = self.db.batch_sql(sql,arr)
        
        return flag     