from flask import Flask, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
#from werkzeug.routing import BaseConverter

app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')
db = SQLAlchemy(app)


#load modules
#index views
from job.web.views import web_views
#users views
from job.users.views import users_views
#users center
from job.users.center import users_center

from job.users.operation import users_operation
#email mail
#from job.email.mail import  email_mail

app.register_blueprint(web_views)
app.register_blueprint(users_views)
app.register_blueprint(users_center)
app.register_blueprint(users_operation)

"""
 file to lager
"""
@app.errorhandler(413)
def error_413(error):
    return '<script>alert(111);</script>'

app.debug = app.config['DEBUG']

if __name__ == '__main__':
    print 'We are running flask via main()'
    app.run()