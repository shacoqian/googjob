#-*- coding:utf-8 -*-
import json

from flask import (Blueprint, render_template, session, url_for, request, g, redirect)
from forms import PlanForm, Pcomment, Comment_form, Info_form, Passwd_form, Say_form, Say_comment_form
from job import db
#from sqlalchemy  import func
from models import Plan, User_record, Supervise, User, \
    Comment, Actation, Collection, Plan_comment, Say, Say_comment
from job.public.upload import upload_img
from center import getUserInfo
from job.public.common import getRecord
from views import getPasswd
from job.email.mail import send_mail
#图片上传大小限制
from job import app
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024



"""
用户中心
处理输入类信息
"""

users_operation = Blueprint('operation', __name__, url_prefix='/users')

@users_operation.before_request
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

    if g.user == None:
       return  redirect('/login')


@users_operation.route('/makeplan' ,methods = ['GET','POST'])
def make_plan():
    form = PlanForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.email.data != '':
            supervise = addSupervise(form,g.user)
            plan = addPlan(form,g.user,supervise)

            #发送EMAIL
            subject = g.user.nickname+u'邀请您监督他的计划'
            info = u'<p>亲爱的用户您好：</p>   <p>'+g.user.nickname+u'在<a href="http://yqplan.com">计划网</a>发布了计划:</p>'+ \
                    u'<p><a href="http://yqplan.com/plan/'+str(plan.id)+'">'+plan.title+u'</a></p>'+ \
                   u'<p>诚挚的邀请您监督他的计划，他在计划中写道：</p><p>'+plan.description+ \
                   u'</p><p>希望您能帮助他克服困难，完成目标！给于我们最诚挚的感谢,谢谢！</p>'
            data = []
            data.append(form.email.data)
            send_mail(subject,data,info)
        else:
            plan = addPlan(form,g.user,None)
        data = {'u_id':g.user.id,'type':1,'plan':plan}
        addUserRecord(data)
        db.session.commit()
        ret = {}
        ret['status'] = 0
        ret['url'] = url_for('center.index')
        return json.dumps(ret)

    return render_template('web/users/center/makeplan.html', \
            userInfo=getUserInfo(g.user, g.user.id ), user=g.user, \
            form=form,records=getRecord())


#创建计划
def addPlan(form,user,supervise=None):
    p = Plan(user, form.title.data, form.description.data,supervise)
    db.session.add(p)
    db.session.flush()    # 主要是这里，写入数据库，但是不提交
    return p

#创建监督人
def addSupervise(form,user):
    s = Supervise(user.id, form.email.data)
    db.session.add(s)
    db.session.flush()
    return s

#用户记录
def addUserRecord(data):
    ur = User_record(data['u_id'], data['type'],data['plan'])
    db.session.add(ur)

@users_operation.route('/editpic/', methods= ['GET', 'POST'])
def editpic():
    if request.method == 'POST':
        result = upload_img(request.files['pic'],g.user.id)
        print 1111
        print result
        if result['code'] == 0:
            g.user.pic = result['filename']
            db.session.commit()
            return "<script>parent.callback(0,'上传成功');</script>"
        else:
            return "<script>parent.callback("+str(result['code'])+",'"+result['message']+"');</script>"


@users_operation.route('/editinfo/', methods= ['GET', 'POST'])
def editinfo():
    form = Info_form(request.form)
    if request.method == 'POST' and form.validate():
        g.user.nickname = form.nickname.data
        g.user.realname = form.realname.data
        g.user.qq = form.qq.data
        g.user.phone = form.phone.data
        db.session.commit()
        return '0'
    return render_template('web/users/center/edit_info.html',user=g.user, \
                userInfo=getUserInfo(g.user, g.user.id ),records=getRecord())

@users_operation.route('/editpasswd/', methods= ['GET', 'POST'])
def editpasswd():
    form = Passwd_form(request.form)
    if request.method == 'POST' and form.validate():
        if (form.passwd1.data != form.passwd2.data):
            return '2' #两次密码输入不同
        newPasswd = getPasswd(form.passwd.data,g.user.salt)
        if (newPasswd != g.user.password):
            return '1' #旧密码错误
        g.user.password = newPasswd
        db.session.commit()
        return '0'
    return render_template('web/users/center/edit_passwd.html',user=g.user, \
                userInfo=getUserInfo(g.user, g.user.id ),records=getRecord())

#关注 status =1  取消关注 status =0
@users_operation.route('/actation/<int:id>/<int:status>/')
def actation(id=0, status = 1):
    if id == 0:
        return '1'
    actation = Actation.query.filter(Actation.uf_id == id, \
                Actation.u_id == g.user.id).first()

    if status == 1:
        if actation == None:
            user = User.query.filter(User.id == id).first()
            if user != None:
                actation = Actation(g.user,user)
                db.session.add(actation)
                db.session.commit()
                return '0'
            else:
                return '1'
        else:
            return '2'
    else:
        if actation != None:
            db.session.delete(actation)
            db.session.commit()
            return '3'
        else:
            return '1'

#收藏
@users_operation.route('/collection/<int:user_id>/<int:plan_id>/')
def setCollection(user_id=0, plan_id=0,):
    if plan_id == 0 or user_id == 0:
        return '1'
    collection = Collection.query.filter(Collection.u_id == user_id, \
                    Collection.p_id == plan_id).first()
    if not collection:
        plan = Plan.query.filter(Plan.id == plan_id).first()
        if not plan:
            return '2'
        else:
            c = Collection(user_id, plan)
            db.session.add(c)
            if plan.collection_num == None:
                plan.collection_num = 0
            plan.collection_num += 1
    else:
        if collection.plan.collection_num == None:
            collection.plan.collection_num = 0
        if  collection.plan.collection_num  > 0:
            collection.plan.collection_num -= 1
        db.session.delete(collection)
    db.session.commit();
    return '0'


@users_operation.route('/plan_comment/', methods=['POST'])
def plan_comment():
    form = Pcomment(request.form)
    status = 1
    if request.method == 'POST' and form.validate():
        p = Plan_comment(form.p_id.data, form.content.data)
        db.session.add(p)
        db.session.flush()
        plan = Plan.query.filter(Plan.id == form.p_id.data).first()
        if plan.plan_comment_num == None:
            plan.plan_comment_num = 0
        plan.plan_comment_num += 1
        u = User_record(g.user.id,2,plan,p)
        db.session.add(u)
        db.session.commit()
        status = 0
        if (plan.supervise != None):
            #发送EMAIL
            subject = g.user.nickname+u'跟进了他的计划'
            info = u'<p>亲爱的用户您好：</p>   <p>'+g.user.nickname+u'在<a href="http://yqplan.com">计划网</a>跟进了计划:</p>'+ \
                    u'<p><a href="http://yqplan.com/plan/'+str(plan.id)+'">'+plan.title+u'</a></p>'+ \
                   u'<p>他在跟进中写道：</p><p>'+p.content+ \
                   u'</p><p>希望您能继续关注，帮助他克服困难，完成目标！给于我们最诚挚的感谢,谢谢！</p>'
            data = []
            data.append(plan.supervise.email)
            send_mail(subject,data,info)

    return json.dumps(status)

@users_operation.route('/comment/', methods=['POST'])
def comment():
    user = g.user
    form = Comment_form(request.form)
    status = 1
    if request.method == 'POST' and form.validate():
        c = Comment(form.p_id.data, form.content.data, user)
        #计划评论数
        plan = Plan.query.filter(Plan.id == form.p_id.data).first()
        if plan.comment_num is None:
            plan.comment_num = 0
        plan.comment_num += 1

        db.session.add(c)
        db.session.flush()
        #插入记录
        record = User_record(user.id, 3, plan, None, c)
        db.session.add(record)
        db.session.commit()
        status = 0
    return json.dumps(status)

#说说
@users_operation.route('/dosay/', methods=['POST'])
def dosay():
    form = Say_form(request.form)
    if request.method == 'POST' and form.validate():
        s = Say(g.user,form.content.data)
        db.session.add(s)
        db.session.flush();
        ur = User_record(g.user.id, 4,None,None,None,s)
        db.session.add(ur)
        db.session.commit()
        return '0'

@users_operation.route('/say_comment/', methods=['POST'])
def say_comment():
    form = Say_comment_form(request.form)
    if request.method == 'POST' and form.validate():
        say = Say.query.filter(Say.id == form.say_id.data).first()
        if say.say_comment_num == None:
            say.say_comment_num = 0
        say.say_comment_num += 1
        s = Say_comment(say,form.content.data,g.user)
        db.session.add(s)
        db.session.flush()
        ur = User_record(g.user.id, 5,None,None,None,say,s)
        db.session.add(ur)
        db.session.commit()
        return '0'

@users_operation.route('/delsay/<int:user_id>/<int:id>/', methods=['GET'])
def delsay(user_id, id):
    if user_id != g.user.id or id == 0:
        return '1' # 错误
    say = Say.query.filter(Say.id == id).first()
    if say == None:
        return '1'
    #删除say
    ur = User_record.query.filter(User_record.s_id == say.id).all();
    if ur != []:
        for item in ur:
            db.session.delete(item)
    say_com =  Say_comment.query.filter(Say_comment.say_id == say.id).all()
    #删除say的留言
    if say_com != []:
        for item1 in say_com:
            db.session.delete(item1)
    db.session.delete(say)
    db.session.commit()
    return '0'

@users_operation.route('/delplan/<int:user_id>/<int:id>/', methods=['GET'])
def delplan(user_id, id):
    if user_id != g.user.id or id == 0:
        return '1' # 错误
    plan = Plan.query.filter(Plan.id == id).first()
    if plan == None:
        return '1'


    #删除Plan和 plan的跟进 plan的留言
    ur = User_record.query.filter(User_record.p_id == plan.id).all();
    if ur != []:
        for item in ur:
            db.session.delete(item)
    #跟进
    plan_com = Plan_comment.query.filter(Plan_comment.p_id == plan.id).all();
    if plan_com != []:
        for item in plan_com:
            db.session.delete(item)
    com = Comment.query.filter(Comment.p_id == plan.id).all()
    if com != []:
        for item in com:
            db.session.delete(item)
    #关于此条计划的收藏
    collection = Collection.query.filter(Collection.p_id == plan.id).all()
    if collection != []:
        for item in collection:
            db.session.delete(item)

    db.session.delete(plan)
    db.session.commit()
    return '0'