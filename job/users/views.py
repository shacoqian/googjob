#-*- coding:utf-8 -*-
import random
import string
import hashlib
import base64
import json
import time

from flask import (Blueprint, render_template, request,redirect,url_for, session, g)
from job.users.models import User
from job import db
from forms import LoginForm, RegisterForm
from job import app
from job.email.mail import send_mail
from flask import make_response


"""
登录注册
"""

users_views = Blueprint('users', __name__, url_prefix='')

@users_views.before_request
def before_request():
    try:
        if session.has_key('signin'):
            g.user = User.query.filter(User.id == session['user_id']).first()
        elif request.cookies.get('user_id') != None:
            g.user = User.query.filter(User.id == request.cookies.get('user_id')).first()
            if g.user != None:
                session['signin'] = True
                session['user_id'] = g.user.id
        else:
            g.user = None
    except:
       g.user = None

@users_views.route('/login', methods = ['GET','POST'])
def index():
    next = request.referrer
    if next == None:
        next = '/index'
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        ret = {'status':1,'message':''}
        email = form.email.data
        password = form.passwd.data
        userInfo = User.query.filter(User.email == email).first()
        if userInfo and userInfo.status == 1:
            if getPasswd(password, userInfo.salt) == userInfo.password :
                session['signin'] = True
                session['user_id'] = userInfo.id
                ret['status'] = 0
            else:
                ret['message'] = '您的账号和密码不匹配'
        else:
            ret['message'] = '您的账号不存在或者未激活！'

        resp = make_response(json.dumps(ret))
        if ret['status']== 0 and form.remember.data:
            resp.set_cookie('user_id', value=str(userInfo.id),max_age=3600*24*7)
        return resp

    return  render_template("web/users/login.html",form = form, next=next, user=g.user)

@users_views.route('/login_out')
def login_out():
    try:
        session['signin'] = False
        session['user_id'] = ''
        user_id = request.cookies.get('user_id')
        print type(user_id)
        #request.cookies.pop('user_id', None)
    except:
        pass
    return redirect('/')

@users_views.route('/register/', methods = ['GET', 'POST'])
def register():
    next = request.referrer
    if next == None:
        next = '/index'
    form = RegisterForm(request.form)
    if request.method == 'POST' and  form.validate():
        data = {}
        salt = getSalt()
        password = getPasswd(form.passwd.data, salt)

        if not check_user(form.email.data):
            u = User(form.email.data, password,salt,form.nickname.data)
            db.session.add(u)
            db.session.commit()
            data['status'] = 0
            #直接登录
            session['sign'] = True
            session['user_id'] = u.id
            """
            #发送email
            activation_email = base64.b64encode(form.email.data)
            activation_url = app.config['WEB_DOMAIN']+'/activation/'+activation_email;
            subject = '感谢您注册计划网，请点击邮件中的激活链接来激活你的账号'
            mail_list = [form.email.data]
            info = '<p>感谢您注册计划网</p><p>您的激活链接是:</p><p>'+activation_url+'</p>'
            send_mail(subject, mail_list, info)
            """
        else:
            data['status'] = 1
            data['detail'] = '用户名已经注册过，您可以尝试找回密码！'
        return json.dumps(data)
    return render_template("web/users/register.html",title='',form = form, next=next, user=g.user)

def check_user(email):
    result = User.query.filter(User.email == email).first()
    if result is None or result.status == 0:
        return False
    else:
        return True

#生成密码
def getPasswd(passwd, salt):
    password = hashlib.md5(salt+passwd).hexdigest()
    return password;

#生成随机字符串
def getSalt():
    item_arr = []
    for i in range(app.config['LENGTH']):
        item_arr.append(random.choice(app.config['SALT_STR']))
    return ''.join(item_arr)

@users_views.route('/success')
def success():
    return render_template('web/users/success.html')


@users_views.route('/activation/<email>/')
def activation(email):
    message = ''
    subTitle = u'激活失败'
    try:
        email = base64.b64decode(email)
        ret = User.query.filter(User.email == email ).first()
        if ret is None :
            message = u'您激活的用户不存在！'
        elif ret.status == 1:
                message = u'您的用户已经激活，请勿重复激活！'
        else:
            ret.status = 1;
            db.session.commit()
            message = u'亲爱的用户，恭喜你激活成功！现在你可以登录我们的网站了！'
            subTitle = u'激活成功'

    except :
        message = u'您的链接无效!'

    return render_template('web/users/activation.html', message = message, subTitle = subTitle)