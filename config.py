# -*- coding:utf-8 -*-

""" configuration of AUN
"""

import os
from datetime import timedelta


class Config(object):
    DEBUG = False
    TESTING = False

    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # flask-wtf CSRF
    CSRF_ENABLED = True
    SECRET_KEY = 'May AU forever'

    # flask-sqlalchemy 配置
    # SQLALCHEMY_POOL_SIZE = 15
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
    # 发件人如('sicun','1412511544@qq.com')
    MAIL = ('华中大社联社团网', 'aunet@auhust.net')
    # 设置session的过期时间
    PERMANENT_SESSION_LIFETIME = timedelta(hours=6)


class ProductionConfig(Config):
    """
    config for production env
    """
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:abc201314@localhost/aunet_flask"
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:abc201314@localhost/aunet_flask"


class DevelopmentConfig(Config):
    """
    config for development env
    """
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    # flask-sqlalchemy 配置
    path = os.path.join(BASEDIR, "test.db")
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+path
    SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
