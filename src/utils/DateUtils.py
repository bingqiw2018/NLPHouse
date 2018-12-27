#coding=utf-8 
'''
Created on 2018年6月7日

@author: bingqiw
'''
import time
import random
import datetime

def get_unit_id():
    now_time = int(round(time.time() * 1000 * 1000000)) + random.randint(0,1000000)
    return str(now_time)

def current_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def current_ftime(format):
    return datetime.datetime.now().strftime(format)

def is_current_fdate(date, format):
    old_date = time.strptime(date,format)
    old_date = time2str(old_date,'%Y-%m-%d')
    old_date = str2time(old_date, '%Y-%m-%d')
    
    curr_date = time.strftime('%Y-%m-%d', time.localtime())
    curr_date = time.mktime(time.strptime(curr_date,'%Y-%m-%d'))
    return old_date == curr_date

def time2str(times,format):
    if type(times) == type(time.time()):
        return time.strftime(format, time.localtime(times))
    else:    
        return time.strftime(format, times)
    
def str2time(times,format):
    return time.mktime(time.strptime(times,format))
       
def cmp_time(new, old):
    return new > old

def cmp_str_time(new, old, format):
    print new,old
    t_new = time.mktime(time.strptime(new,format))
    t_old = time.mktime(time.strptime(old,format))
    return t_new > t_old