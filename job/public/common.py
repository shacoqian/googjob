#-*- coding:utf-8 -*-

#合并字典

from job.users.models import User_record

def dictMerged(item1, item2, pre=''):
    for k in item1:
        try:
            item2[k]
            item2[pre+k] = item2[k]
            del item2[k]
        except KeyError:
            pass
    item1.update(item2)
    del item2
    return item1


#获取最新动态
def getRecord():
    news = User_record.query.order_by(' id desc ').limit(5).all();
    return news

