from wtforms  import Form, TextField, BooleanField,PasswordField, validators

class RegisterForm(Form):
    email = TextField('email', [validators.DataRequired(), validators.Email()])
    passwd = PasswordField('passwd', [validators.Length(min=6, max=40)])
    nickname = TextField('nickname', [validators.Length(min=1, max=40)])

    
class LoginForm(Form):
    email = TextField('email', [validators.DataRequired(), validators.Email()])
    passwd = PasswordField('passwd', [validators.Length(min=6, max=40)])
    remember = BooleanField('remember')


class PlanForm(Form):
    title = TextField('title', [validators.DataRequired(),validators.Length(min=6, max=200)])
    description = TextField('description',[validators.DataRequired(),validators.Length(min=6)])
    #public = TextField('public',[validators.DataRequired()])
    email = TextField('email')


class Pcomment(Form):
    p_id = TextField('p_id', [validators.DataRequired()])
    content = TextField('content', [validators.Length(min=1, max=200)])

class Comment_form(Form):
    p_id = TextField('p_id', [validators.DataRequired()])
    content = TextField('content', [validators.Length(min=1, max=200)])

class Info_form(Form):
    nickname = TextField('nickname', [validators.Length(max=40)])
    realname = TextField('realname', [validators.Length(max=40)])
    qq = TextField('qq')
    phone = TextField('phone')

class Passwd_form(Form):
    passwd = PasswordField('passwd', [validators.Length(min=6, max=40)])
    passwd1 = PasswordField('passwd1', [validators.Length(min=6, max=40)])
    passwd2 = PasswordField('passwd2', [validators.Length(min=6, max=40)])

class Say_form(Form):
    content = PasswordField('content', [validators.Length(min=1, max=200)])

class Say_comment_form(Form):
    say_id = TextField('say_id', [validators.DataRequired()])
    content = TextField('content', [validators.Length(min=1, max=200)])

