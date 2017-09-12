#-*-coding:utf-8-*-

""" package aun
"""

from datetime import timedelta
import pymysql
from flask import Flask, session, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_principal import Principal
from flask_restful import Api
from flask_msearch import Search
from jieba.analyse.analyzer import ChineseAnalyzer


aun_db = SQLAlchemy()
aun_mail = Mail()
aun_login = LoginManager()
aun_principals = Principal()
aun_api = Api()
aun_search = Search(analyzer=ChineseAnalyzer(), db=aun_db)


def create_app(config):
    """
    create flask create_app
    """
    app = Flask(__name__)  # 创建应用
    app.config.from_object(config)

    aun_db.init_app(app)
    aun_mail.init_app(app)
    aun_login.init_app(app)
    aun_principals.init_app(app)
    aun_api.init_app(app)
    aun_search.init_app(app)

    from aun.home import home
    from aun.admin import aun_admin
    from aun.material import material
    # 注册蓝图
    app.register_blueprint(home)
    app.register_blueprint(aun_admin, url_prefix='/admin')
    app.register_blueprint(material)

    return app


# 实例化各扩展

aun_login.login_view = ''  # TODO not determined


# 设置cookie的过期时间
aun_login.remember_cookie_duration = timedelta(hours=6)

from aun import views
from aun.sign_up import views
from aun.admin import views
from aun.association import views
from aun.data_station import views
from aun.home import views
