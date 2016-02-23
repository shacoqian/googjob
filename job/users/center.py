#-*- coding:utf-8 -*-
"""
@description  user center
@author       qianfeng5511@163.com
"""
import json
from flask import (Blueprint, render_template, \
                   request,redirect, session, url_for, g )
from job import db
from sqlalchemy  import func
from models import Plan, User_record, User, \
     Actation, Collection, Say
from job.public.pages import getListNum
from job.public.common import getRecord

import copy
users_center = Blueprint('center', __name__, url_prefix='/users')


"""
用户中心
处理显示类信息
"""

@users_center.before_request
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

@users_center.route('/')
@users_center.route('/index/')
@users_center.route('/index/<int:user_id>/')
@users_center.route('/<int:user_id>/')
@users_center.route('/index/<int:user_id>/<int:page>/')
@users_center.route('/<int:user_id>/<int:page>/')
def index(user_id = 0, page = 1):
    userInfo = getUserInfo(g.user, user_id )
    if not userInfo:
        return redirect('/')
    #分页URL
    preUrl = userInfo['u_url']
    #获取分页信息
    pageInfo = getListNum( getActivityCount(userInfo['id']), preUrl ,page)

    #获取活动列表
    datas = getUserActivity(userInfo['id'],pageInfo, ' id desc ')

    title = userInfo['nickname']
    return render_template('web/users/center/index.html', user= g.user, \
            userInfo=userInfo, datas=datas, pageInfo = pageInfo, \
            records=getRecord(), title=title)


@users_center.route('/myplan/')
@users_center.route('/myplan/<int:user_id>/')
@users_center.route('/myplan/<int:user_id>/<int:page>/')
def myplan(user_id=0, page =1):
    userInfo = getUserInfo(g.user, user_id )
    if not userInfo:
        return redirect('/')

    preUrl = '/users/myplan/'+str(userInfo['id'])+'/'
    count = db.session.query(func.count(Plan.id)).\
        filter(Plan.u_id == userInfo['id']).scalar()
    pageInfo = getListNum( count, preUrl ,page)

    datas = Plan.query.filter(Plan.u_id == userInfo['id'] ) \
        .order_by('id desc').offset(pageInfo['offset'])\
        .limit(pageInfo['limit']).all()
    title = userInfo['nickname']
    return render_template('web/users/center/myplan.html',user=g.user, \
                    userInfo=userInfo, datas=datas, pageInfo=pageInfo, \
                    records=getRecord(), title=title)

#我的说说
@users_center.route('/mysay/')
@users_center.route('/mysay/<int:user_id>/')
@users_center.route('/mysay/<int:user_id>/<int:page>/')
def mysay(user_id=0, page =1):
    userInfo = getUserInfo(g.user, user_id )
    if not userInfo:
        return redirect('/')

    preUrl = '/users/mysay/'+str(userInfo['id'])+'/'
    count = db.session.query(func.count(Say.id)).\
        filter(Say.u_id == userInfo['id']).scalar()
    pageInfo = getListNum( count, preUrl ,page)

    datas = Say.query.filter(Say.u_id == userInfo['id'] ) \
        .order_by('id desc').offset(pageInfo['offset'])\
        .limit(pageInfo['limit']).all()

    title = userInfo['nickname']
    return render_template('web/users/center/mysay.html',user=g.user, \
                    userInfo=userInfo, datas=datas, pageInfo=pageInfo, \
                    records=getRecord(), title=title)

#我的收藏
@users_center.route('/mycollection/')
@users_center.route('/mycollection/<int:user_id>/')
@users_center.route('/mycollection/<int:user_id>/<int:page>/')
def myCollection(user_id=0, page = 1):
    userInfo = getUserInfo(g.user, user_id )
    if not userInfo:
        return redirect('/')
    preUrl = '/users/mycollection/'+str(userInfo['id'])+'/'
    count = db.session.query(func.count(Collection.id)).\
        filter(Collection.u_id == userInfo['id']).scalar()
    pageInfo = getListNum( count, preUrl ,page)

    datas = Collection.query.filter(Collection.u_id == userInfo['id'] ) \
        .order_by('id desc').offset(pageInfo['offset'])\
        .limit(pageInfo['limit']).all()
    title = userInfo['nickname']
    return render_template('web/users/center/mycollection.html',user=g.user, \
                    userInfo=userInfo, datas=datas, pageInfo=pageInfo, \
                    records=getRecord(),title=title)
#获取userInfo
def getUserInfo(user, user_id):
    if not user and user_id == 0:
        return False
    elif not user:
        userInfo = User.query.filter(User.id == user_id).first().__dict__
        userInfo['follow'] = 0
    elif user != None and (user_id == user.id or user_id == 0 ):
        userInfo = copy.deepcopy(user.__dict__)
    elif user_id != user.id and user_id != 0:
        userInfo = User.query.filter(User.id == user_id).first().__dict__
        actation = Actation.query.filter(Actation.uf_id == userInfo['id'], \
                Actation.u_id == g.user.id).first()
        if actation != None:
            userInfo['follow_status'] = 1
        else:
            userInfo['follow'] = 0

    userInfo['u_url'] = '/users/'+str(userInfo['id'])+'/'
    #获取关注
    userInfo['follow'] = getFollow(userInfo['id'],1,1)
    #获取粉丝
    userInfo['fans'] = getFans(userInfo['id'],1,1)
    return userInfo

#获取关注信息
@users_center.route('/follow/')
@users_center.route('/follow/<int:user_id>/')
@users_center.route('/follow/<int:user_id>/<int:page>/')
def getFollow(user_id=0, page=1,info=0):
    if user_id == 0:
        return redirect('/')
    count = db.session.query(func.count(Actation.id)).\
        filter(Actation.u_id == user_id).scalar()
    if info == 1:
        follow = Actation.query.filter(Actation.u_id == user_id) \
            .order_by('id desc').limit(12).all()
        return {'count':count, 'follow':follow}
    else:
        userInfo = getUserInfo(g.user, user_id )
        if not userInfo:
            return redirect('/')
        preUrl = '/users/follow/'+str(userInfo['id'])+'/'
        pageInfo = getListNum( count, preUrl ,page)

        datas = Actation.query.filter(Actation.u_id == user_id ) \
            .order_by('id desc').offset(pageInfo['offset'])\
            .limit(pageInfo['limit']).all()
    title = userInfo['nickname']
    return render_template('web/users/center/follow.html',user=g.user, \
                    userInfo=userInfo, datas=datas, pageInfo=pageInfo, \
                    records=getRecord(),title=title)

#获取粉丝
@users_center.route('/fans/')
@users_center.route('/fans/<int:user_id>/')
@users_center.route('/fans/<int:user_id>/<int:page>/')
def getFans(user_id=0, page=1,info=0):
    if user_id == 0:
        return redirect('/')
    count = db.session.query(func.count(Actation.id)).\
        filter(Actation.uf_id == user_id).scalar()
    if info == 1:
        fans = Actation.query.filter(Actation.uf_id == user_id) \
            .order_by('id desc').limit(12).all()
        return {'count':count, 'fans':fans}
    else:
        userInfo = getUserInfo(g.user, user_id )
        if not userInfo:
            return redirect('/')
        preUrl = '/users/follow/'+str(userInfo['id'])+'/'
        pageInfo = getListNum( count, preUrl ,page)

        datas = Actation.query.filter(Actation.uf_id == user_id ) \
            .order_by('id desc').offset(pageInfo['offset'])\
            .limit(pageInfo['limit']).all()
    title = userInfo['nickname']
    return render_template('web/users/center/fans.html',user=g.user, \
                    userInfo=userInfo, datas=datas, pageInfo=pageInfo, \
                    records=getRecord(),title=title)


#获取用户活动列表
def getUserActivity(u_id,pageInfo,order_by):
    activity = User_record.query.filter(User_record.u_id == u_id)\
        .order_by(order_by).offset(pageInfo['offset']).limit(pageInfo['limit']).all()
    return activity

def getActivityCount(u_id):
    ur = User_record(u_id)
    return ur.count_record()


