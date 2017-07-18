#-*-coding:utf-8-*-

""" package aun
"""

from datetime import timedelta
import pymysql
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_principal import Principal
from flask_restful import Api

aun_app = Flask(__name__)  # 创建应用
aun_app.config.from_object('config')  # 导入配置
try:
    aun_app.config.from_object('secret_config')  # 导入secret配置
except:
    pass

# 实例化各扩展
aun_db = SQLAlchemy(aun_app)
aun_mail = Mail(aun_app)

aun_login = LoginManager()
aun_login.init_app(aun_app)
aun_login.login_view = ''  # TODO not determined

aun_principals = Principal(aun_app)

aun_api = Api(aun_app)

from aun.home import home
from aun.admin import aun_admin

# 注册蓝图
aun_app.register_blueprint(home)
aun_app.register_blueprint(aun_admin, url_prefix='/admin')


# 设置session和cookie的过期时间
aun_app.permanent_session_lifetime = timedelta(hours=6)
aun_login.remember_cookie_duration = timedelta(hours=6)

from aun import views
