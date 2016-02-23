#-*- coding:utf-8 -*-
from PIL import Image
import os
import time

width = 50
height = 50
img_ext = ['jpg', 'gif', 'png']
img_path = '/static/upload/head/'

def upload_img(file, id):
    ext = checkImgExt(file.filename)
    if not ext:
        return error(1)
    image = Image.open(file)
    size = image.size
    if size[0] < width or size[1] < height:
        return error(2)
    realpath = os.path.dirname(os.path.dirname(__file__)).replace('\\','/')
    img_dir = realpath + img_path
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    filename = img_path+str(id)+'-'+str(int(time.time()))+'.'+ext
    image.thumbnail((200, 200), Image.ANTIALIAS)
    image.save(realpath+filename)
    return {'code':0, 'filename':filename}

def checkImgExt(filename):
    fileExt = filename.split('.')
    ext = fileExt[len(fileExt)-1].lower()
    if(ext in img_ext):
        return ext
    else:
        return False

def error(code):
    if code == 1:
        return {'code':1, 'message':u'扩展名错误，请重新上传！'}
    if code == 2:
        return {'code':2,'message':u'图片尺寸过小,请重新上传！'}
