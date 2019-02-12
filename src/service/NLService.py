#coding=utf-8 
'''
Created on 2018年6月20日
LDAService，即LDA主题分析服务，对文章的主题进行分析
@author: bingqiw
'''

from src.dao.NLDao import NLDao
import jieba
import jieba.posseg as jp
import jieba.analyse as ja
from gensim import corpora, models, similarities
from src.utils import DateUtils as du
from BaseService import BaseService

class GrammerUtil(BaseService):
    
    def initParam(self, params={}, dao=NLDao()):
        BaseService.initParam(self,params, dao)
        jieba.load_userdict(self.param['user_dict'])
        ja.set_stop_words(self.param['stop_words'])
    
    def getDictionByList(self, str_list):
        
        dictionary = corpora.Dictionary(str_list)
        featureNum=len(dictionary.token2id.keys())#提取词典特征数
        
        corpus = [dictionary.doc2bow(dic) for dic in str_list]
        
        tfidfModel = models.TfidfModel(corpus)
        similarModel = similarities.SparseMatrixSimilarity(tfidfModel[corpus],num_features=featureNum)
        
        return dictionary ,tfidfModel, similarModel
        
        
    def getAnalysisList(self, str_list, word, withPrint=False, withWeight=False, withResult=True):
        
        text_list = []
        
        if len(str_list) > 0:
            for str_item in str_list:
                data = jieba.lcut(str_item)
                text_list.append(data)
    
        dictionary = corpora.Dictionary(text_list)
        featureNum=len(dictionary.token2id.keys())
        corpus = [dictionary.doc2bow(text) for text in text_list]
        tfidfModel = models.TfidfModel(corpus)
        
        if withWeight :
            corpus_tfidf = tfidfModel[corpus]
            for doc in corpus_tfidf:
                print(doc)

        new_vec = self.getNewVecByDic(dictionary, word)
        
        similarModel = similarities.SparseMatrixSimilarity(tfidfModel[corpus],num_features=featureNum)
        sim = similarModel[tfidfModel[new_vec]]
        
        if withPrint :
            for text in str_list:
                print "原词：["+text+"]"
            print "新词：["+word+"]"
            
        if withResult :
            for i in range(len(sim)):
                print("查询与第"+str(i+1)+"句话的相似度为:"+str(sim[i]))
        
        return text_list, dictionary, tfidfModel, sim
        
    def getNewVecByDic(self, dictionary, word):
        new_arr = jieba.lcut(word)
        new_vec = dictionary.doc2bow(new_arr)
        return new_vec
    
    def getLdaWordList(self,word, topK=5):
        tags = "/".join(ja.extract_tags(word, topK))
        return tags.split("/")
        
#   解析词汇，合词增频      
    def parseWords(self, str_p):    
        words = jp.lcut(str_p)    
        index = 0
#             print("/".join(word+flag for word,flag in words)) 
        for word, flag in words:
            if flag == 'r' : #如果是代词
                self.__addTag(index,words,word)
            index += 1  
              
    def __addTag(self, index, words, word):       
        if index == 0 :
            return
                
        left_index = index - 1
        list_t = []
        
        for i in range(index):
            item = words[left_index]
            if item.flag.find('n') != -1:
                list_t.append(item.word)
                left_index -=1  
            else:
                break
        
        if len(list_t)>0:
            list_t.reverse()
            str_t = "".join(list_t)
            jieba.add_word(str_t, 2 ,"nz")
#             print word+"="+str_t
        
        right_index = index + 1
        max = len(words)
        list_t = []
        
        for i in range(right_index, max):
            item = words[i]
            if item.flag.find('n') != -1:
                list_t.append(item.word)
            else:
                break
            
        if len(list_t)>0:
            str_t = "".join(list_t)
            jieba.add_word(str_t, 2 ,"nz")
#             print word+"="+str_t

class NLService(BaseService):
    
    __SIMILAR_LIMIT = 0.05
    
    __gUtil = GrammerUtil()
    
    def initParam(self, params={}, dao=NLDao()):
        BaseService.initParam(self,params, dao)
    
    def queryLdaDic(self):
        self.__queryLdaDic()
        
    def __queryLdaDic(self):
        
        ds = NLDao()    
        
        param = {}
        q_list = ds.queryLdaDic(param)
        
        dic_list = []
        for item in q_list:
            v_list = item['value']
            dic_list.append(v_list)   
            print "/".join(v_list)    
        
        dictionary ,tfidfModel, similarModel = self.__gUtil.getDictionByList(dic_list)
        return dictionary,similarModel,tfidfModel,q_list
    
    def doLdaPsgLearn(self, param):
        print "主题熟知分析开始 ..."
        dictionary, matrixSimilarity, tfidf, d_list = self.__queryLdaDic()
        
        q_list = self.dao.queryDocPsgForPsgLearn(param)
        print "学习规模："+str(len(q_list))
        
        limit_flag = self.__SIMILAR_LIMIT
        print "相似度门限："+str(limit_flag)
        count = 0
        
        param_list = []
        word_not_in_dic = []
        word_not_lda = []        
        
        for item in q_list:
            
            psg_content = item['psg_content']
            
            self.__gUtil.parseWords(psg_content)
            
            new_vec = self.__gUtil.getNewVecByDic(dictionary, psg_content)
            psg_keywords = "/".join(self.__gUtil.getLdaWordList(psg_content))
            
            dic_keywords_str = ''
            sim_ratios_str = ''
            domain_keywords_str = ''
            sim_limit_str = '0'
            
            if len(new_vec) > 0:
                sim = matrixSimilarity[tfidf[new_vec]]
                
                dic_keywords = []
                domain_keywords = []
                sim_ratios = []
                
                for index in range(len(sim)):
                    if sim[index] > limit_flag:
                        dic_keywords.append(",".join(d_list[index]['value']))
                        domain_keywords.append(d_list[index]['key'])
                        sim_ratios.append(sim[index])
                        
                        print "["+item['psg_content']+"]匹配到："+d_list[index]['key'] +"，门限："+ str(sim[index])
                        count += 1
                    else:
                        word_not_lda.append(psg_content)    
#                 param_list.append({'psg_id':item['psg_id'], 'doc_id':item['doc_id'], 'dic_keywords':"/".join(dic_keywords), 'psg_keywords':psg_keywords, 'similar_limit':limit_flag, 'similar_ratio':0,  'domain_keyword':"/".join(domain_keywords)})
                dic_keywords_str += "/".join(dic_keywords)
                sim_ratios_str += "/".join(sim_ratios)
                domain_keywords_str += "/".join(domain_keywords)
                sim_limit_str += str(self.__SIMILAR_LIMIT)
            else:
                word_not_in_dic.append(psg_content)    
            
            data_tt = {'psg_id':item['psg_id'], 'doc_id':item['doc_id'], 'dic_keywords':dic_keywords_str, 'psg_keywords':psg_keywords, 'similar_limit':sim_limit_str, 'similar_ratio':sim_ratios_str,  'domain_keyword':domain_keywords_str}    
            param_list.append(data_tt)        
        
        print "不在主题词典里的内容数量："+ str(len(word_not_in_dic))       
        print "没有匹配的内容数量："+ str(len(word_not_lda))        
        print "成功对接段落数量："+str(count)                
        print "非对接段落数量："+str(len(q_list) - count)           
            
        try:
            count = self.dao.updateDocPsgForPsgLearn(param_list)
            print "获得主题段落领域信息："+str(count)
        except BaseException as ex:
            print "except:" +str(ex)
        
        result = False
        if count > 0:
            result = True
        else:
            print "没有主题段落，学习从此退出！！！"    
                
        #建立章节字典
        return result
    
#         从媒体文章中提取主题，并根据已有的主题字典，判断领域归属，获得匹配领域标识，建立关联
    def doMediaLearn(self, param):
        
        print "主题领域分析开始 ..."
        dictionary, matrixSimilarity, tfidf, d_list = self.queryLdaDic()
        
        q_list = self.dao.queryDocCatalogsForMeidaLearn(param)
        print "学习规模："+str(len(q_list))
        #分词
        
        limit_flag = self.__SIMILAR_LIMIT
        print "相似度门限："+str(limit_flag)
        count = 0
        
        param_list = []
        for item in q_list:
#             print "item['title']="+item['title']
            title_arr = ja.extract_tags(item['title'])
                        
            generate = " ".join(title_arr)
#             print generate
            new_title_arr = generate.split()
            new_vec = dictionary.doc2bow(new_title_arr)
            
            if len(new_vec) > 0:
                sim = matrixSimilarity[tfidf[new_vec]]
                for index in range(len(sim)):
                    if sim[index] > limit_flag:
                        print "["+item['title']+"]匹配到："+d_list[index]['key'] +"，门限："+ str(sim[index])
                        count += 1
                        param_list.append({'doc_id':item['doc_id'], 'keywords':"/".join(title_arr), 'similar_limit':limit_flag, 'similar_ratio':sim[index], 'domain_id':d_list[index]['tr_id'],  'domain_keyword':d_list[index]['key']})
            
            
                        
        print "成功对接领域数量："+str(count)                
        print "非对接领域数量："+str(len(q_list) - count)                
        
        result = False
        
        if count > 0:
            try:
                count = self.dao.updateDocCatalogsForMeidaLearn(param_list)
                print "获得主题目录领域信息："+str(len(count))
                result = True
            except BaseException as ex:
                    print "except:" +ex
        else:
            print "没有对接领域，学习从此退出！！！"    
        #建立章节字典
        return result
    
    def getDocPsgForPsgLearn(self, param):
        count = self.dao.getDocPsgForPsgLearn(param)
        return count
        
    def getDocCatalogsForMeidaLearn(self, param):
        count = self.dao.getDocCatalogsForMeidaLearn(param)
#         flag = True if count>0 else False
        flag = False
        
        if count > 0 :
            flag = True

        print "提取媒体待学习的章节目录："+str(flag)
        return flag
    
#     根据媒体主题分析结果，更新主题字典
    def refreshLdaDicByMedia(self, param):    
        
        print "查询主题字典，构建新的主题字典"
        
        flag = True
        try:
            nl_doc_cata_list, nl_dic_word_list = self.dao.queryLdaDicByMedia(param)
            doc_map = self.__getNewDicByMedia(nl_doc_cata_list, nl_dic_word_list)
            self.__refreshLdaDicByMedia(doc_map)
        except BaseException as ex:
            print('except:', ex)
            flag = False
        
        print "建立新的主题字典完毕！"
        return flag
    
    def __refreshLdaDicByMedia(self,doc_map):
        
        print "建立主题词袋 ，并且更新主题字典 ..."
        
        for key in doc_map.keys():
            domain_words = doc_map.get(key)
            dictionary = corpora.Dictionary(domain_words)
            
            data = []
            for k in dictionary.iterkeys():
                item = {'dic_id':k, 'word_group':key, 'dic_word':dictionary.get(k), 'word_freq':dictionary.dfs[k], 'create_time':du.current_time()}
                data.append(item)
            
            ds = NLDao()   
            ds.refreshLdaDic(key, data)
                
        
    def __getNewDicByMedia(self,nl_doc_cata_list, nl_dic_word_list):    
        
#       媒体目录表数据  
        doc_map = {}
        for item in nl_doc_cata_list:
            domain_name = item['domain_keyword']
            domain_keywords = item['keywords']
            
            if doc_map.has_key(domain_name):
                doc_list = doc_map[domain_name]
                doc_list.append(domain_keywords.split('/'))
            else:
                doc_list = []
                doc_list.append(domain_keywords.split('/'))
                doc_map[domain_name] = doc_list
                
#       主题字典表
        for item in nl_dic_word_list:
            domain_name = item['word_group']
            domain_keywords = item['dic_word']    
            
            if doc_map.has_key(domain_name):
                doc_list = doc_map[domain_name]
                doc_list.append(domain_keywords.split('/'))
            else:
                doc_list = []
                doc_list.append(domain_keywords.split('/'))
                doc_map[domain_name] = doc_list
            
        print "建立领域主题词汇 :"   + str(len(doc_map.iterkeys()))
         
        return doc_map
    
    
class NLAnalysis(BaseService):
    
    def initParam(self, params={}, dao=NLDao()):
        BaseService.initParam(self,params, dao)
        jieba.load_userdict(self.param['user_dict'])
        ja.set_stop_words(self.param['stop_words'])
    
    def __parseWords(self, str_p):    
        words = jp.lcut(str_p)    
        index = 0
#             print("/".join(word+flag for word,flag in words)) 
        for word, flag in words:
            if flag == 'r' : #如果是代词
                self.__addTag(index,words,word)
            index += 1  
              
    def __addTag(self, index, words, word):       
        if index == 0 :
            return
                
        left_index = index - 1
        list_t = []
        
        for i in range(index):
            item = words[left_index]
            if item.flag.find('n') != -1:
                list_t.append(item.word)
                left_index -=1  
            else:
                break
        
        if len(list_t)>0:
            list_t.reverse()
            str_t = "".join(list_t)
            jieba.add_word(str_t, 2 ,"nz")
            print word+"="+str_t
        
        right_index = index + 1
        max = len(words)
        list_t = []
        
        for i in range(right_index, max):
            item = words[i]
            if item.flag.find('n') != -1:
                list_t.append(item.word)
            else:
                break
            
        if len(list_t)>0:
            str_t = "".join(list_t)
            jieba.add_word(str_t, 2 ,"nz")
            print word+"="+str_t
           
#   对目前的目录标题进行分析     
    def anlysisTitleDoc(self, isWeight = True):
        q_list = self.dao.queryTitleDoc({})
        
        for item in q_list:
            temp_str = item['title']
            
            self.__parseWords(temp_str)
            
            words = jp.cut(temp_str)
            words_extract = ja.extract_tags(temp_str,withWeight=isWeight,topK=20)
            words_text = ja.textrank(temp_str,withWeight=isWeight,topK=20)
             
            print temp_str  
#             print("/".join(jieba.cut(temp_str)))
            print("/".join(word+flag for word, flag in words))
#             print("/".join(word[0]+str(word[1]) for word in words_extract))
#             print("/".join(word[0]+str(word[1]) for word in words_text))
            print("="*100)    
    
        
#     根据目录的标题来分析主题
#     param = {'source':'toutiao.com','keyword':u'中医按摩'}
    def analyseLdaByTitle(self,param):      
        
        data = self.dao.queryDocCatalogs(param)
        
        jieba.load_userdict("C:/Python27/Lib/site-packages/jieba/dict_my.txt")
        ja.set_stop_words("C:/Python27/Lib/site-packages/jieba/stopword_my.txt")
        
        str_title_list = []
        for index in range(len(data)): 
            title = ja.extract_tags(data[index]['title'],allowPOS=('nt','nz','nr','ns', 'n', 'vn', 'v','j'),topK=20)
    #         print data[index]['title']
            str_title_list.append(title)
    #     print "data size="+ str(len(str_title_list) )  
        
        dictionary = corpora.Dictionary(str_title_list)
        print "dictionary size:"+str(len(dictionary.keys())) 
        
        self.__importLdaDic(dictionary, param)
        return dictionary
    
    def __importLdaDic(self, dictionary, param):
        
        data = []
        for key in dictionary.iterkeys():
            item = {'dic_id':key, 'word_group':param['domain_name'], 'dic_word':dictionary.get(key), 'word_freq':dictionary.dfs[key], 'create_time':du.current_time()}
            data.append(item)
        ds = NLDao()    
        ds.importLdaDic(data)
        
    # 解析词性
    def __parsePosseg(self):
        
        ds = NLDao()   
        param = {'source':'toutiao.com','keyword':u'中医按摩'}
        data = ds.queryDocCatalogs(param)
        jieba.load_userdict("C:/Python27/Lib/site-packages/jieba/dict_my.txt")
        ja.set_stop_words("C:/Python27/Lib/site-packages/jieba/stopword_my.txt")
        
        for index in range(len(data)): 
            words = jp.cut(data[index]['title'])
            print ("/".join(word+flag for word, flag in words) )
            print data[index]['abstract']
    
    def __printDict(self,dictionary):  
        dicts = dict(dictionary.items())
        dfs = dictionary.dfs
        for key in dicts:  
            print key,str(dicts[key]),dfs[key]
             
        # 基于文章标题，分析文章主题        
        # print str(dictionary)
        # print "字典，{单词id，在多少文档中出现}"  
        # print dictionary.dfs #字典，{单词id，在多少文档中出现}  
        # print "文档数目"  
        # print dictionary.num_docs #文档数目  
        # print "dictionary.items()"  
        # print_dict(dict(dictionary.items())) #  
        # print "字典，{单词id，对应的词}"  
        # print_dict(dictionary.id2token) #字典，{单词id，对应的词}  
        # print "字典，{词，对应的单词id}"  
        # print_dict(dictionary.token2id) #字典，{词，对应的单词id}  
        # print "所有词的个数"  
        # print dictionary.num_pos #所有词的个数  
        # print "每个文件中不重复词个数的和"  
        # print dictionary.num_nnz #每个文件中不重复词个数的和 
        # print "过滤掉出现频率最高的N个单词" 
        # print dictionary.filter_n_most_frequent(20) 
        # param = {'source':'toutiao.com','keyword':u'中医按摩'}
    
    def __similarCheck(self, dictionary, data, str_title_list):
        
        # 5.基于词典建立新的语料库
        corpus = [dictionary.doc2bow(text) for text in str_title_list]
    #     print corpus
        tfidf = models.TfidfModel(corpus)
        
#         tfidf_corpus =  tfidf[corpus]
        
    #     print tfidf_corpus
    
        doc_list = ['中医按摩','中医','按摩','穴位']
        
        new_vec = dictionary.doc2bow(doc_list)
        print new_vec
        
        featureNum=len(dictionary.token2id.keys())#提取词典特征数
        index = similarities.SparseMatrixSimilarity(tfidf[corpus],num_features=featureNum)
        sim = index[tfidf[new_vec]]
        for i in range(len(sim)):
#             doc = data[i]
    #         print("查询与第"+str(i+1)+"句话的相似度为:"+str(sim[i]))
    #         print("与文章("+doc['doc_id']+","+doc['title']+")的相似度为:"+str(sim[i]))
            print sim[i]
    
    #   遍历字典
    def __viewDic(self,dictionary):   
        print dictionary
        
        for key in dictionary.iterkeys():
            print key,dictionary.get(key),dictionary.dfs[key]
            
    #   将一片文章的分词，加入到词袋，words = ["中医推拿"], words即划分完词的一段文章   
    def __addWordToDic(self,dictionary, words): 
        dictionary.doc2bow(words,allow_update = True)
        
    #   将一组文章的分词，加入词袋，documents=[["中医针灸"]]    
    def __addDocToDic(self,dictionary,documents):
        dictionary.add_documents(documents)
        
    