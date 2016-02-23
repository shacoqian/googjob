#-*- coding:utf-8 -*-
from flask import (Blueprint, render_template, session, url_for, request, g, redirect)
from job.users.models import Plan, User, Collection, Plan_comment, Comment, Say, Say_comment
from job import db
from sqlalchemy import func
from job.public.pages import getListNum
from sqlalchemy  import func
from job.public.common import getRecord
import json

web_views = Blueprint('index', __name__)

@web_views.before_request
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

@web_views.route('/')
def index():
    if g.user != None:
        return redirect('/index/')
    return render_template("web/index.html")

@web_views.route('/index')
@web_views.route('/index/<int:page>/')
@web_views.route('/index/')
def show(page = 1):
    param = {}
    search = request.args.get('search')
    if search == None:
        search = ''
    else:
        param = {'search':search}

    count = db.session.query(func.count(Plan.id))
    plan = Plan.query
    if search != None:
        count = count.filter(Plan.title.like('%'+search+'%'))
        plan = plan.filter(Plan.title.like('%'+search+'%'))
    count = count.scalar()

    sort = request.args.get('sort')
    if sort == 'comment':
        plan = plan.order_by('comment_num desc')
        param.update({'sort':'comment'})
    elif sort == 'plan_comment':
        plan = plan.order_by('plan_comment_num desc')
        param.update({'sort':'plan_comment'})
    elif sort == 'collection':
        plan = plan.order_by('collection_num desc')
        param.update({'sort':'collection'})
    else:
        plan = plan.order_by('id desc')
    preUrl = '/index/'
    pageInfo = getListNum( count, preUrl ,page,param)

    plan = plan.offset(pageInfo['offset']).limit(pageInfo['limit']).all()
    title = u'计划列表'
    return render_template('web/default/index.html', user = g.user,
        pageInfo=pageInfo, plan=plan, search=search,records=getRecord(), \
        title=title,sort=sort)


@web_views.route('/plan/')
@web_views.route('/plan/<int:id>')
@web_views.route('/plan/<int:id>/<int:ppage>/')
@web_views.route('/plan/<int:id>/<int:ppage>/<int:cpage>/')
def plan(id=0, ppage =1, cpage =1):
    if (id == 0):
       return '11';

    #计划内容
    plan = Plan.query.filter(Plan.id == id).first()
    if plan is None:
        return '22'
    if plan.clicks is None:
        plan.clicks = 0
    plan.clicks = plan.clicks+1
    db.session.commit()

    #计划跟进
    count = db.session.query(func.count(Plan_comment.id)).\
        filter(Plan_comment.p_id == plan.id).scalar()
    pageUrl = '/plan/'+str(plan.id)+'/'
    pageInfo = getListNum(count, pageUrl, ppage)
    plan_comment = Plan_comment.query.filter(Plan_comment.p_id == plan.id).\
        order_by(' id desc ').offset(pageInfo['offset']).\
        limit(pageInfo['limit']).all()

    #计划评论
    ccount = db.session.query(func.count(Comment.id)). \
        filter(Comment.p_id == plan.id).scalar()
    pageUrl = pageUrl+str(ppage)+'/'
    cpageInfo = getListNum(ccount, pageUrl, cpage)

    comment = Comment.query.filter(Comment.p_id == plan.id, \
        ).order_by(' id desc '). \
        offset(cpageInfo['offset']).limit(cpageInfo['limit']).all()

    datas = comment
    #获取收藏状态
    collection_status = getCollection(plan.id)

    title = plan.title
    return render_template('web/default/plan.html', user=g.user, plan=plan,
                plan_comment=plan_comment, pageInfo=pageInfo, datas=datas, \
                cpageInfo=cpageInfo,collection_status=collection_status, \
                records=getRecord(), title=title)
"""
def getChildComment(comment,i=-1):
    datas = []
    i+=1
    for item in comment:
        item_com = Comment.query.filter(Comment.parent_id == item.id).all()
        item = [item,i]
        item.append(getChildComment(item_com,i))
        datas.append(item)
    return datas
"""

#获取是否收藏
def getCollection(plan_id):
    if g.user == None:
        return False
    else:
        c = Collection.query.filter(Collection.u_id == g.user.id, Collection.p_id == plan_id).first()
        if c == None:
            return False
        else:
            return True

@web_views.route('/say')
@web_views.route('/say/<int:page>/')
@web_views.route('/say/')
def say(page = 1):
    count = db.session.query(func.count(Say.id))
    say = Say.query
    count = count.scalar()

    preUrl = '/say/'
    pageInfo = getListNum( count, preUrl ,page)
    say = say.order_by('id desc').offset(pageInfo['offset']). \
        limit(pageInfo['limit']).all()
    title = u'说说列表'
    return render_template('web/default/say.html',user = g.user,records=getRecord(), \
                say=say, pageInfo=pageInfo, title=title )

@web_views.route('/sayfeed/<int:id>/')
@web_views.route('/sayfeed/<int:id>/<int:page>')
@web_views.route('/sayfeed/<int:id>/<int:page>/')
def sayfeed(id=0, page=1):
    if id == 0:
        return redirect('/')
    say = Say.query.filter(Say.id == id).first()
    if say.clicks == None:
        say.clicks = 0
    say.clicks += 1
    db.session.commit()
    #计划评论
    count = db.session.query(func.count(Say_comment.id)). \
        filter(Say_comment.say_id == id).scalar()
    pageUrl = '/sayfeed/'+str(id)+'/'
    pageInfo = getListNum(count, pageUrl, page)

    datas = Say_comment.query.filter(Say_comment.say_id == id, \
        ).order_by(' id desc '). \
        offset(pageInfo['offset']).limit(pageInfo['limit']).all()
    title = say.content
    return render_template('web/default/sayfeed.html',user = g.user,records=getRecord(), \
            say=say, datas=datas ,pageInfo=pageInfo,title=title)