#coding=utf-8 
'''
Created on 2018年7月14日

@author: bingqiw
'''
from BaseDao import BaseDao

class SpiderDao(BaseDao):
    
    def getDocCatalogs(self, doc_list):
        
        sql = "insert sp_doc_catalogs (doc_id,source,doc_type,sp_type,title,abstract,article_url,image_url,comment_count,datetime,create_time,keyword,media_name,tag,tag_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        arr = []
        
        query_sql = "select t.doc_id from sp_doc_catalogs t where t.source=%s and t.media_name=%s and t.keyword=%s and t.title=%s"
        query_arr = []
         
        for doc in doc_list:
            arr.append([doc['doc_id'],doc['source'],doc['doc_type'],doc['sp_type'],doc['title'],doc['abstract'],doc['article_url'],doc['image_url'],doc['comment_count'],doc['datetime'],doc['create_time'],doc['keyword'],doc['media_name'],doc['tag'], doc['tag_id']])
            query_arr.append([doc['source'],doc['media_name'],doc['keyword'],doc['title']])
    #         print arr
        
        reCount = self.db.batch_sql(query_sql, query_arr)
        print "判断搜索文档目录是否已经存在这些文章？"+str(reCount)
        flag = -1
        if reCount == 0 :
            flag = self.db.batch_sql(sql,arr)
            print "入库完毕"
        else:
            print "现有文档已经保存过相关文档"
        return flag  
    
    #   根据媒体号，抓取文章目录
    def getMediaCatalogs(self, doc_list):
        
        sql = '''
        insert sp_doc_catalogs
        (doc_id, source, doc_type, sp_type, title, article_url, image_url, view_num, comment_count, datetime, create_time, media_name, media_id) VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)    
        '''
        arr = []
         
        for doc in doc_list:
            arr.append([doc['doc_id'],doc['source'],doc['doc_type'],doc['sp_type'],doc['title'],doc['article_url'],doc['image_url'],doc['view_num'],doc['comment_count'],doc['datetime'],doc['create_time'],doc['media_name'],doc['media_id']])
            
    #         print arr
        flag = self.db.batch_sql(sql,arr)
        print "入库完毕"
        return flag   
    
    def querySessionKeywords(self, param):
        spider_id = param['spider_id']
        sql = "select t.session_id, t.words, t.other_id from nl_session_words t "
        consult = "WHERE t.other_id = %s order by t.create_time desc limit 1"
        result = []
        
        if param and len(param)>0:
            arr = []
            arr.append(spider_id)
            sql += consult    
            result = self.db.select( sql, arr)
        else:
            print 'param is none, service quit !!!'        
                
        return result
    
    # 查询头条的媒体号
    def queryToutiaoMediaUser(self, param):
        sql = "select t.media_id, t.media_name, t.source, t.img_url, t.user_url, t.keywords, t.create_time, t.remark from sp_media_user t"
        cond = " where t.media_type='0' "
        
        result = []
        if param and len(param)>0:
            arr = []
            
            isCond = False
            
            if 'source' in param.keys() :
                arr.append(param['source'])
                cond += " and t.source=%s "
                isCond = True
                
            if 'create_time' in param.keys():
                arr.append(param['create_time'])
                cond += " and date_format(t.create_time,'"+param['format']+"')=%s "
                isCond = True
            
            if 'media_id' in param.keys() :
                arr.append(param['media_id'])
                cond += " and t.media_id=%s "
                isCond = True
            
            if 'media_name' in param.keys() :
                arr.append(param['media_name'])
                cond += " and t.media_name=%s "
                isCond = True
                    
            if isCond :
                sql += cond
            
            result = self.db.select( sql, arr)
        else:
            print 'param is none, service quit !!!'    
        
        return result
    
    # 查询没有导入目录的媒体号
    def queryToutiaoMediaUserUnDone(self, param):
        sql = "select t.* from sp_media_user t  "
        cond = " where t.media_type='0' and t.media_id not in (select distinct media_id from sp_doc_catalogs where media_id is not null) "
        
        result = []
        if param and len(param)>0:
            arr = []
            
            isCond = False
            
            if 'source' in param.keys() :
                arr.append(param['source'])
                cond += " and t.source=%s "
                isCond = True
                
            if 'create_time' in param.keys():
                arr.append(param['create_time'])
                cond += " and date_format(t.create_time,'"+param['format']+"')=%s "
                isCond = True
            
            if 'media_id' in param.keys() :
                arr.append(param['media_id'])
                cond += " and t.media_id=%s "
                isCond = True
            
            if 'media_name' in param.keys() :
                arr.append(param['media_name'])
                cond += " and t.media_name=%s "
                isCond = True
                    
            if isCond :
                sql += cond
            
            result = self.db.select( sql, arr)
        else:
            print 'param is none, service quit !!!'    
        
        return result    
    
    def queryDocCatalogsWithoutPassages(self, param):
        sql = "select t.*  from sp_doc_catalogs t "
        cond = " where t.MEDIA_ID IS NOT NULL AND t.doc_id not in (select distinct doc_id from sp_doc_passages) "
        arr = []
        if param and len(param)>0:
            isCond = False
            
            if 'media_name' in param.keys() :
                arr.append(param['source'])
                cond += " and t.media_name=%s "
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
        else:
            print 'param is none'    
            sql += cond
            
        result = self.db.select(sql, arr)
        return result
    
    def getDocPassages(self,doc_list):
        sql = "insert sp_doc_passages (psg_id, doc_id, psg_order, psg_content, create_time, psg_keywords) VALUES (%s,%s,%s,%s,%s,%s)" 
           
        arr = []
         
        for doc in doc_list:
            arr.append([doc['psg_id'],doc['doc_id'],doc['psg_order'],doc['psg_content'],doc['create_time'],doc['psg_keywords']])
            
        flag = self.batch_sql(sql,arr)
        print "入库完毕"
        return flag      
            