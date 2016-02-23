#-*- coding:utf-8 -*-
#@author qianfeng@5511@163.com

from job import db
from job.users import constants as USER
from datetime import  datetime
from sqlalchemy import  func

class User(db.Model):
    """
    USER TABLE
    用户表
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(USER.MAX_USERNAME))
    email = db.Column(db.String(USER.MAX_EMAIL))
    password = db.Column(db.String(USER.MAX_PASSW))
    created_time = db.Column(db.DateTime, default=datetime.now )
    status = db.Column(db.SmallInteger, default=USER.ALIVE)
    salt = db.Column(db.String(5))
    nickname = db.Column(db.String(200))
    pic = db.Column(db.String(255))
    realname = db.Column(db.String(100))
    qq = db.Column(db.String(15))
    phone = db.Column(db.String(15))

    def __init__(self, email, password, salt, nickname):
        self.email = email
        self.password = password
        self.salt = salt
        self.nickname = nickname

    def __repr__(self):
        return '<User %r>' % (self.email)

class Supervise(db.Model):
    """
    Supervise table
    监督人表
    """
    __tablename__ = 'supervise'
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer)
    email = db.Column(db.String(100))
    status = db.Column(db.SmallInteger, default=1)
    created_time = db.Column(db.DateTime, default=datetime.now )

    def __init__(self,u_id, email):
        self.u_id = u_id
        self.email = email


    def __repr__(self):
        return '<Supervise %r>' % (self.email)

class Plan(db.Model):
    """
    plan table
    计划表
    """
    __tablename__ = 'plan'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text())
    status = db.Column(db.SmallInteger, default=1 )
    created_time = db.Column(db.DateTime, default=datetime.now)
    public = db.Column(db.SmallInteger, default=1 )
    clicks = db.Column(db.Integer, default=0)
    comment_num = db.Column(db.Integer, default=0)
    plan_comment_num = db.Column(db.Integer, default=0)
    collection_num = db.Column(db.Integer, default=0)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', primaryjoin=(u_id==User.id), \
            backref=db.backref('userInfo', lazy='dynamic'))
    s_id = db.Column(db.Integer, db.ForeignKey('supervise.id'))
    supervise = db.relationship('Supervise', primaryjoin=(s_id==Supervise.id), \
            backref=db.backref('supervise', lazy='dynamic'))

    def __init__(self, user,title, description,supervise=None):
        self.user = user
        self.title = title
        self.description = description
        if supervise != None:
            self.supervise = supervise

    def __repr__(self):
        return '<Plan %r>' % (self.title)

#计划跟进
class Plan_comment(db.Model):

    __tablename__ = 'plan_comment'
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer)
    content = db.Column(db.Text())
    created_time = db.Column(db.DateTime, default=datetime.now )

    def __init__(self,p_id,content):
        self.p_id = p_id
        self.content = content

    def __repr__(self):
        return '<Plan_comment %r>' % (self.p_id)

#评论表
class Comment(db.Model):

    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer)
    content = db.Column(db.Text())
    created_time = db.Column(db.DateTime, default=datetime.now )

    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',primaryjoin=(u_id==User.id), \
            backref=db.backref('user', lazy='dynamic'))

    def __init__(self, p_id, content, user):
        self.p_id = p_id
        self.content = content
        self.user = user

    def __repr__(self):
        return '<Comment %r>' % (self.id)

class Collection(db.Model):
    """
    collerction
    收藏表
    """
    __tablename__ = 'collection'
    id = db.Column(db.Integer, primary_key = True)
    u_id = db.Column(db.Integer)
    p_id = db.Column(db.Integer, db.ForeignKey('plan.id'))
    plan = db.relationship('Plan', \
            backref = db.backref('plan1', lazy='dynamic'))
    created_time = db.Column(db.DateTime, default=datetime.now )

    def __init__(self, u_id, plan):
        self.u_id = u_id
        self.plan = plan

    def __repr__(self):
        return '<Collection %r>' %(self.u_id)


class Actation(db.Model):
    """
    关注表
    """
    __tablename__ = 'actation'
    id = db.Column(db.Integer, primary_key = True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user1 = db.relationship('User', primaryjoin=(u_id==User.id), \
            backref=db.backref('user1', lazy='dynamic'))

    uf_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', primaryjoin=(uf_id==User.id), \
            backref=db.backref('user2', lazy='dynamic'))

    created_time = db.Column(db.DateTime, default=datetime.now )

    def __init__(self, user1, user):
        self.user1 = user1
        self.user = user

    def __repr__(self):
        return '<Actation %r>' %(self.u_id)

class Say(db.Model):
    """
    说说表
    """
    __tablename__ = 'say'
    id = db.Column(db.Integer, primary_key = True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', primaryjoin=(u_id==User.id), \
            backref=db.backref('users', lazy='dynamic'))
    content = db.Column(db.Text())
    say_comment_num = db.Column(db.Integer, default=0)
    clicks = db.Column(db.Integer, default=0)
    created_time = db.Column(db.DateTime, default=datetime.now )

    def __init__(self, user, content):
        self.user = user
        self.content = content

    def __repr__(self):
        return '<Say %r>' %(self.u_id)

class Say_comment(db.Model):
    """
    说说留言
    """
    __tablename__ = 'say_comment'
    id = db.Column(db.Integer, primary_key=True)
    say_id = db.Column(db.Integer, db.ForeignKey('say.id'))
    say = db.relationship('Say', primaryjoin=(say_id==Say.id), \
            backref=db.backref('says', lazy='dynamic'))
    content = db.Column(db.Text())
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',primaryjoin=(u_id==User.id), \
            backref=db.backref('sc_user', lazy='dynamic'))
    created_time = db.Column(db.DateTime, default=datetime.now )

    def __init__(self, say, content, user):
        self.say = say
        self.content = content
        self.user = user

    def __repr__(self):
        return '<Say_comment %r>' % (self.id)




class User_record(db.Model):
    """
    user_record table
    用户操作记录表
    """
    __tablename__ = 'user_record'
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #type 是记录类型 1是计划 2跟进 3留言 4说说
    type = db.Column(db.SmallInteger, default=1)
    created_time = db.Column(db.DateTime, default=datetime.now )

    #t_id 如果type为1 则存计划的ID 以此类推
    p_id = db.Column(db.Integer, db.ForeignKey('plan.id'))
    plan = db.relationship('Plan', \
            backref = db.backref('planInfo', lazy='dynamic'))
    c_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    comment = db.relationship('Comment',\
            backref = db.backref('commentInfo', lazy='dynamic'))
    pc_id = db.Column(db.Integer, db.ForeignKey('plan_comment.id'))
    plan_comment = db.relationship('Plan_comment', \
            backref=db.backref('plan_comment', lazy='dynamic'))
    s_id = db.Column(db.Integer, db.ForeignKey('say.id'))
    say = db.relationship('Say', primaryjoin=(s_id == Say.id),\
            backref=db.backref('say', lazy='dynamic'))
    sc_id = db.Column(db.Integer, db.ForeignKey('say_comment.id'))
    say_comment = db.relationship('Say_comment', primaryjoin=(sc_id == Say_comment.id),\
            backref=db.backref('say_comment', lazy='dynamic'))

    def __init__(self, u_id, type=1, plan=None, plan_comment=None, comment=None, say = None, say_comment=None):
        self.u_id = u_id
        self.type = type
        if plan is not None:
            self.plan = plan
        if plan_comment is not None:
            self.plan_comment = plan_comment
        if comment is not None:
            self.comment = comment
        if say is not None:
            self.say = say
        if say_comment is not None:
            self.say_comment = say_comment

    def count_record(self):
        total = 0
        count = db.session.query(func.count(User_record.id))
        if self.u_id:
            total = count.filter(User_record.u_id == self.u_id ).scalar()
        return total


    def __repr__(self):
        return '<User_record %r>' % (self.t_id)
