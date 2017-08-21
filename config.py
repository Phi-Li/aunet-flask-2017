# -*- coding:utf-8 -*-

""" configuration of AUN
"""

import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DEBUG = True


# flask-wtf CSRF

CSRF_ENABLED = True
SECRET_KEY = 'May AU forever'


# flask-sqlalchemy 配置

# SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
SQLALCHEMY_DATABASE_URI = 'sqlite://///home/lyjdwh/Documents/AUN/test.db'
# SQLALCHEMY_DATABASE_URI =
# 'mysql+pymysql://root:abc201314@localhost/aunet_flask'  # mysql的配置

SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')

#SQLALCHEMY_POOL_SIZE = 15
SQLALCHEMY_POOL_RECYCLE = 15
SQLALCHEMY_TRACK_MODIFICATIONS = True


# flask-mail SMTP server

# MAIL_SERVER='smtp.qq.com'
MAIL_SERVER = 'smtp.exmail.qq.com'  # 邮箱服务器
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'aunet@auhust.net'  # 如果是qq邮箱则为qq号，136邮箱同理
MAIL_PASSWORD = '@4W<tS5.m]gQ'  # 客户端密码
MAIL = ('华中大社联社团网', 'aunet@auhust.net')  # 发件人如('sicun','1412511544@qq.com')
