#-*- coding:utf-8 -*-
from __future__ import division
from job import app
import math


#获取分页信息
def getListNum(count, url, page=1,param={}):
    page = int(page)
    perPage = app.config['PER_PAGE']
    total_page = math.ceil(count/perPage)
    if total_page < page:
        page = total_page

    if page < 1:
        page = 1;

    offset = (page -1)*perPage

    param = getUrlParam(param)
    return {'page':page,'total_page':int(total_page),'count':count, \
            'offset':offset,'limit':perPage,'url':url,'param':param}

def getUrlParam(param):
    if param == {}:
        return ''
    else:
        data =[]
        string = ''
        for k in param:
            string = str(k)+'='+param[k]
            data.append(string)
        urlStr = '&'.join(data)
        return urlStr