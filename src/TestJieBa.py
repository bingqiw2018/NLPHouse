#coding=utf-8 
'''
Created on 2018年6月20日

@author: bingqiw
'''
import jieba.analyse
import jieba.posseg
import jieba.posseg as jp
from src.service.NLService import NLService, GrammerUtil

def div_word_test():
    print '-'*60

    testSentence = "利用python进行数据分析"
    
    print("1.精准模式分词结果："+"/".join(jieba.cut(testSentence,cut_all=False)))
    print("2.全模式分词结果："+"/".join(jieba.cut(testSentence,cut_all=True)))
    print("3.搜索引擎模式分词结果："+"/".join(jieba.cut_for_search(testSentence)))
    print("4.默认（精准模式）分词结果："+"/".join(jieba.cut(testSentence)))

def load_user_word_lib():
    
    testSentence=u"简书书院是一个很好的交流平台"
    print("1.加载词典前分词结果：")
    for item in jieba.posseg.cut(testSentence):
        print(item.word+"---"+item.flag)
#     print([item for item in jieba.posseg.cut(testSentence)])
    print '-'*60
    
    jieba.load_userdict("C:/Python27/Lib/site-packages/jieba/dict_my.txt")
    print("2.加载词典后分词结果：")
    for item in jieba.posseg.cut(testSentence):
        print(item.word+"---"+item.flag)
    
#   动态调整词库和词频，改变划词方式
def load_word_config():    
    print("1.原始分词结果："+"/".join(jieba.cut("数据分析与数据挖掘的应用", HMM=False)))
    print '-'*60
    
    jieba.add_word("的应用")
    print("2.使用add_word(word, freq=None, tag=None)结果："+"/".join(jieba.cut("数据分析与数据挖掘的应用", HMM=False)))
    
    print '-'*60
    jieba.suggest_freq("的应用",tune=True)
    print("3.使用suggest_freq(segment, tune=True)结果："+"/".join(jieba.cut("数据分析与数据挖掘的应用", HMM=False)))

import jieba.analyse as ja

# 基于TF-IDF算法的关键词抽取
# TFIDF的主要思想是：如果某个词或短语在一篇文章中出现的频率TF高，并且在其他文章中很少出现，则认为此词或者短语具有很好的类别区分能力，适合用来分类。
# jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=()) 
# –sentence 为待提取的文本 
# –topK 为返回几个 TF/IDF 权重最大的关键词，默认值为 20 
# –withWeight 为是否一并返回关键词权重值，默认值为 False 
# –allowPOS 仅包括指定词性的词，默认值为空，即不筛选
# 主要思想：将文本内容进行分词，并加权，主要目的是突出文本的主题
# 这里要注意加权策略
# 1、主语、定语一般为名词，权重高，
# 2、相同关键字的词频越高，权重就越高；
def abstract_tags_tf_idf(words):
    jieba.load_userdict("C:/Python27/Lib/site-packages/jieba/dict_my.txt")
    ja.set_stop_words("C:/Python27/Lib/site-packages/jieba/stopword_my.txt")
#     jieba.suggest_freq(('肾','属'), True)
#     jieba.suggest_freq("小蛮腰", True)
#     words = "肾属水"
#     print("/".join(jieba.cut("肾属水", HMM=False)))    
#     print("/".join(ja.extract_tags(words)))
#     print("/".join(ja.extract_tags("我喜欢广州广州小蛮腰",3)))
#     print("/".join(ja.extract_tags("我喜欢广州广州广州小蛮腰",3)))

    for word in ja.extract_tags(words,withWeight=True,topK=20):
        print(word[0] +"-"+str(word[1]))

       
# 基于TextRank算法的关键词提取
# jieba.analyse.textrank(sentence, topK=20, withWeight=False, allowPOS=(‘ns’, ‘n’, ‘vn’, ‘v’)) 直接使用，接口相同，注意默认过滤词性。
# jieba.analyse.TextRank() 新建自定义 TextRank 实例 
# –基本思想： 
# 1，将待抽取关键词的文本进行分词 
# 2，以固定窗口大小(默认为5，通过span属性调整)，词之间的共现关系，构建图 
# 3，计算图中节点的PageRank，注意是无向带权图
# 主要思想：将文本内容进行分词，并加权，主要目的是突出文本的主题
# 这里要注意加权策略       
# 关注词与词之间的关系，如果词频相同，就不能记入主题列表，对已经划分主题的，进一步区分类型的较好
def abstract_tags_textrank(words):       
    jieba.load_userdict("C:/Python27/Lib/site-packages/jieba/dict_my.txt")
    ja.set_stop_words("C:/Python27/Lib/site-packages/jieba/stopword_my.txt")
#     words = "Python 结巴分词 关键词抽取分析 - CSDN博客"
#     jieba.suggest_freq("简书书院",True)
#     print words
#     print "/".join(ja.textrank(words,topK=20))
    
    for word in ja.textrank(words,withWeight=True,topK=20):
        print(word[0] +"-"+str(word[1]))

# 词性标注
def poss_tags():
#     jieba.add_word("中医按摩")
    jieba.load_userdict("C:/Python27/Lib/site-packages/jieba/dict_my.txt")
    words = jieba.posseg.cut("按摩三对穴位就能养心养肾，中医的方法不得不服！")
    print ("/".join(word+flag for word, flag in words) )
    
def test_zhongyi():    
    temp_str = "从按摩的治疗上，可分为保健按摩、运动按摩和医疗按摩。"    
    jieba.load_userdict("C:/Python27/Lib/site-packages/jieba/dict_my.txt")
    jieba.suggest_freq(('指','以'), True)
    print("中医分词结果："+"/".join(jieba.cut(temp_str)))
   
    words = jieba.posseg.cut(temp_str)
    print ("/".join(word+flag for word, flag in words) )
    
#     for word in ja.textrank(temp_str,withWeight=True,topK=120):
#         print(word[0] +"-"+str(word[1]))

def takeSecond(elem):
    return elem[2]

# 字典排序        
def viewDic(dictionary):   
    ele_list = []
    for key in dictionary.iterkeys():
        
        if len(dictionary.get(key).strip()) > 0:
            elem = (key, dictionary.get(key), dictionary.dfs[key])
#             print key,dictionary.get(key),dictionary.dfs[key]
            ele_list.append(elem)
    
    #对元祖数组进行排序
    ele_list.sort(key=takeSecond, reverse = True)
    
    for item in ele_list:
        print item[1]

def test001():     
    str = "经常按摩百会穴，提阳气，治脑病，降血压"
    jieba.analyse.set_stop_words("C:/Python27/Lib/site-packages/jieba/stopword_my.txt")
    title_arr = jieba.cut(str)
    print "/".join(title_arr)
    print("/".join(ja.extract_tags(str)))
    
    print "end" 

def parseWords(str_p):    
        words = jp.lcut(str_p)    
        index = 0
#             print("/".join(word+flag for word,flag in words)) 
        for word, flag in words:
            if flag == 'r' : #如果是代词
                addTag(index,words,word)
            index += 1  
              
def addTag(index, words, word):       
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
            
def cixing():    
    temp_str = "据甘肃省质量技术监督局网站《关于下达2018年度第2批地方标准制修订计划的函》，由甘肃省戒毒管理局、甘肃省中医药大学起草的中医按摩戒毒康复技术规范，已列入本批次地方标准制修订计划。    "    
    parseWords(temp_str)
    jieba.load_userdict("C:/Python27/Lib/site-packages/jieba/dict_my.txt")
    words = jieba.posseg.cut(temp_str)
    words_extract = ja.extract_tags(temp_str,withWeight=True,topK=20)
    words_text = ja.textrank(temp_str,withWeight=True,topK=20)
     
    print temp_str  
    print ("/".join(word+flag for word, flag in words))
    print("/".join( word[0] for word in words_extract))
    print("/".join( word[0]+str(word[1]) for word in words_extract))
#     print("/".join(word[0]+str(word[1]) for word in words_text))

def grammer():    
    gUtil = GrammerUtil()
    str_p = "山东小儿推拿李波老师分享宝宝打嗝的中医小儿推拿按摩手法 "    
    
    words = jieba.posseg.cut(str_p)
    words_extract = ja.extract_tags(str_p,withWeight=True,topK=5)
    print ("/".join(word+flag for word, flag in words))
    print("/".join( word[0] for word in words_extract))
    
    gUtil.parseWords(str_p)
    print "-"*100
    words = jieba.posseg.cut(str_p)
    words_extract = ja.extract_tags(str_p,withWeight=True,topK=5)
    print ("/".join(word+flag for word, flag in words))
    print("/".join( word[0] for word in words_extract))

if __name__ == '__main__':
    
    dictionary, matrixSimilarity, tfidf, d_list = NLService().queryLdaDic()
    print dictionary
    new_word = "11月27日上午，甘肃省中医按摩医院正式开业。省残联党组成员、巡视员张恩和，党组成员、副理事长蒋录基、杨润泉、吴小萍，党组成员曾占奎出席揭牌仪式。省中医药管理局副局长李清霞出席仪式并代表省卫计委讲话。张恩和巡视员和李清霞副局长共同为甘肃省中医按摩医院揭牌；杨润泉副理事长致辞；省康复中心医院院长石秀娥介绍省中医按摩医院筹建情况。省中医药大学针推学院等相关医院负责人以及省残联各处室、各中心负责人，省康复中心医院党政班子、中层干部百余人参加仪式。"
    g_util = GrammerUtil()
    new_vec, psg_keywords = g_util.getNewVecByDic(dictionary, new_word)
    print new_word 
    print new_vec 
    sim = matrixSimilarity[tfidf[new_vec]]
    
    for i in range(len(sim)):
        print("".join(psg_keywords)+" 查询与第"+d_list[i]['key']+"句话的相似度为:"+str(sim[i]))
        
    print "end"