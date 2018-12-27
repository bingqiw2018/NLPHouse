#coding=utf-8 
'''
Created on 2018年6月20日

@author: bingqiw
'''
import jieba
import warnings

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
                        
from gensim import corpora, models, similarities
import jieba.analyse as ja

def word_cut():
    
    jieba.load_userdict("C:/Python27/Lib/site-packages/jieba/dict_my.txt")
    # 1.导入句子
    
    sentence1 = "我喜欢吃番薯"
    sentence2 = "番薯是个好东西"
    sentence3 = "利用python进行文本挖掘"
    
    # 2.分词
    data1 = jieba.lcut(sentence1)
    data2 = jieba.lcut(sentence2)
    data3 = jieba.lcut(sentence3)

    # 3.转换格式："词语1 词语2 词语3 … 词语n"
    texts = [data1, data2, data3]
    
#     print ("/".join( word[0] for word in ja.extract_tags(sentence1,withWeight=True,topK=5)))
    
    # 4.基于文本建立词典
    dictionary = corpora.Dictionary(texts)
    featureNum=len(dictionary.token2id.keys())#提取词典特征数
#     dictionary.save("./dictionary.txt")#保存语料库
    
    # 5.基于词典建立新的语料库
    corpus = [dictionary.doc2bow(text) for text in texts]
    # 6.TF-IDF处理
    tfidf = models.TfidfModel(corpus)
    
    # 输出每个句子每个词语的tfidf值
    corpus_tfidf = tfidf[corpus]
    for doc in corpus_tfidf:
        print(doc)

    # 7.加载对比句子并整理其格式
    sentence4 = "吃东西"
    data4 = jieba.lcut(sentence4)
#     print ("/".join( word[0] for word in ja.extract_tags(sentence4,withWeight=True,topK=5)))
    new_vec = dictionary.doc2bow(data4)
    print new_vec
    
    index = similarities.SparseMatrixSimilarity(tfidf[corpus],num_features=featureNum)
    sim = index[tfidf[new_vec]]
    
    for i in range(len(sim)):
        print("查询与第"+str(i+1)+"句话的相似度为:"+str(sim[i]))
    
# 查询与第1句话的相似度为:0.3992843
# 查询与第2句话的相似度为:0.3476831
# 查询与第3句话的相似度为:0.0

if __name__ == '__main__':
    word_cut()
    
    
    
    
    
    