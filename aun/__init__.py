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
from config import DevelopmentConfig, ProductionConfig

#     aun_app.config.from_object('secret_config')  # 导入secret配置
# except:
#     pass

aun_db = SQLAlchemy()
aun_mail = Mail()
aun_login = LoginManager()
aun_principals = Principal()
aun_api = Api()


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

    from aun.home import home
    from aun.admin import aun_admin
    # 注册蓝图
    app.register_blueprint(home)
    app.register_blueprint(aun_admin, url_prefix='/admin')

    return app


aun_app = create_app('config.DevelopmentConfig')
# 实例化各扩展

aun_login.login_view = ''  # TODO not determined


# 设置session和cookie的过期时间
aun_app.permanent_session_lifetime = timedelta(hours=6)
aun_login.remember_cookie_duration = timedelta(hours=6)

from aun import views
