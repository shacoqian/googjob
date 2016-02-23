#-*- coding:utf-8 -*-

import os
_basedir = os.path.abspath(os.path.dirname(__file__))+'\job'

username = 'root'
password = 'eric3yang'
host = '121.40.130.117'
dbname = 'goodjob'

DEBUG = True;



SQLALCHEMY_DATABASE_URI = 'mysql://' +username+':'+password+'@'+host+'/'+dbname
SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')

WTF_CSRF_ENABLED = True;
SECRET_KEY = '123456'

# 密码 salt
LENGTH = 4
SALT_STR = '123456789ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghijklmnpqrstuvwxyz'


#email
MAIL_SERVER = 'smtp.163.com'
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = 'qianfeng5511@163.com'
MAIL_PASSWORD = 'qobushi110'

#发送EMAIL邮箱
ADMIN_MAIL = 'qianfeng5511@163.com'

#网址
WEB_DOMAIN = 'http://121.40.130.117:8080'

PER_PAGE = 15