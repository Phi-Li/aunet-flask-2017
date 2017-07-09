# -*-coding:utf-8 -*-

""" email module docstring
"""

from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from aun import aun_mail, aun_app

MAIL = aun_app.config['MAIL']


def send_async_email(app, msg):
    """ function docstring
    """
    with aun_app.app_context():
        aun_mail.send(msg)


def send_email(subject, recipients, text_body):
    """
    Args:
        subject: 主题
        recipients: 收件人的list
        text_body： 内容
        sender: 发件人，默认为配置中的发件人
    """
    message = Message(subject, sender=MAIL, recipients=recipients)
    message.html = text_body
    thread = Thread(target=send_async_email, args=[app, message])
    thread.start()
