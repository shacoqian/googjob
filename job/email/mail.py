from flask import (Blueprint)
from flask.ext.mail import Message
from job.email import mail
from job import app

email_mail = Blueprint('mail', __name__, url_prefix='')

@email_mail.route('/mail')
def send_mail(subject, mail_list, info):
    sender = app.config['ADMIN_MAIL']
    msg = Message(subject, sender = sender, recipients = mail_list)
    #msg.body = info
    msg.html = info
    mail.send(msg)
    return True;
