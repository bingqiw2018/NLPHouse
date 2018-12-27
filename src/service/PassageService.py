#coding=utf-8 
'''
Created on 2018年8月6日

@author: bingqiw
'''
from BaseService import BaseService
from src.dao.PassageDao import PassageDao
from src.dao.NLDao import NLDao
from src.utils import DateUtils as du
import os
import pandas as pd

class PassageService(BaseService):
    
    def initParam(self, params={}, dao=None):
        BaseService.initParam(self, params, PassageDao())
    
        
    def createCognitionPassages(self, param):    
        
#       获得领域概念，再根据概念找到对应的熟知段落
        conceptList = self.dao.queryConceptForPsg(param)
        
        nlDao = NLDao()
        
        if len(conceptList) > 0:
    #       创建熟知库
            param_list = []
            
            for concept in conceptList:
                param = {}
                param['tr_id'] = du.get_unit_id()
                param['tr_parent_id'] = concept['tr_id']
                param['tr_name'] = concept['tr_name']
                param['create_time'] = du.current_time()
                param_list.append(param)
                
            count = self.dao.createCognitionPassages(param_list)    
            
#           针对每一个概念，熟知段落入文件
            if count>0:
                
                index = 0
                for concept in conceptList:
                    
                    loc_file_path = self.param['loc_file_path']['loc_passage_path']
                    
                    if os.path.exists(loc_file_path):
                        
                        param = {}
                        param['tr_id'] = concept['tr_id']
                        param['tr_name'] = concept['tr_name']
                        param['domain_keyword'] = concept['domain_keyword']
                        nl_psg_list = nlDao.queryDocPsgByConcept(param)
                        
                        if len(nl_psg_list)>0:
                            param = {}
                            tr_psg_id = param_list[index]['tr_id']
                            tr_psg_parent_id = concept['tr_id']
                            psg_path = loc_file_path + "passage_"+tr_psg_id+'_'+tr_psg_parent_id+'.cvs'
                            
                            param['tr_psg_id'] = tr_psg_id
                            param['tr_psg_parent_id'] = tr_psg_parent_id
                            param['psg_path'] = psg_path
                            param['psg_num'] = len(nl_psg_list)
                            
                            if self.__importPsgDataToFile(psg_path, nl_psg_list):
                                count = self.dao.updateCognitionPsg(param)
                                if count > 0:
                                    print "主题段落创建成功：",tr_psg_id,tr_psg_parent_id
                            else:
                                print "文件入库失败！"
                        else:
                            print "没有对应的主题段落..."
                    else:
                        print "文件路径不存在！"
                        break
                    
                    index += 1
                    
            else:
                print "熟知段落创建失效！"
        else:    
            print "没有概念结点！"
            
    def __importPsgDataToFile(self, psg_path, nl_psg_list):    
        
        flag = True
        try:
            df = pd.DataFrame(nl_psg_list)   
            df.to_csv(psg_path,header=None,index=False)
            print "导入成功："+psg_path
        except BaseException as ex:
            print('except:', ex)
            flag = False
        return flag
             