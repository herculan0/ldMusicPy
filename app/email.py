from threading import Thread
from flask import current_app, render_template
from flaks_mail import Message
from . import mail

def enviar_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def enviar_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['LDM_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['LDM_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=enviar_async_email, args[app, msg])
    thr.start()
    return thr
