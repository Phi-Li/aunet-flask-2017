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
    # MAIL_SERVER = 'smtp.exmail.qq.com'  # 邮箱服务器
    MAIL_SERVER = "hustau.cn"
    # MAIL_PORT = 465
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USE_SSL = True
    # MAIL_USERNAME = 'aunet@auhust.net'  # 如果是qq邮箱则为qq号，136邮箱同理
    MAIL_USERNAME = "sicun@hustau.cn"
    MAIL_PASSWORD = 'sicun'  # 客户端密码
    # 发件人如('sicun','1412511544@qq.com')
    MAIL = ('华中大社联社团网', 'sicun@hustau.cn')
    # 设置session的过期时间
    PERMANENT_SESSION_LIFETIME = timedelta(hours=3)

    # flask-msearch
    MSEARCH_INDEX_NAME = 'whoosh_index'
    MSEARCH_BACKEND = 'whoosh'
    MSEARCH_ENABLE = True


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
