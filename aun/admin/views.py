# -*-coding:utf-8 -*-

""" module docstring
"""

# import extensions and python library
import os
from flask import redirect, request, session
from flask_principal import identity_loaded, RoleNeed, UserNeed, ActionNeed
from flask_login import logout_user

# import models
from aun import aun_login, aun_app, aun_api
from aun.admin.news import SlideshowApi, SlideshowsApi,  ArticlesApi, ArticleApi, ArticleDetailApi, TagsApi, TagApi, CategorysApi, CategoryApi
from aun.admin.users import UsersApi, UserApi, RolesApi, RoleApi, NodesApi, NodeApi, CurrentUserApi
from aun.admin.search import SearchArticleApi
from aun.admin.login import LoginApi
from aun.admin.models import User

from aun.admin import aun_admin


basedir = aun_app.config['BASEDIR']


@aun_login.user_loader
def load_user(user_id):
    """ load user to enable flask_login extension
    """
    return User.query.get(int(user_id))


@identity_loaded.connect_via(aun_app)
def on_identity_loaded(sender, identity):
    """ flask-principal load user's permission into session
    """
    try:
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.roleName))

        # Assuming the User model has a list of nodes, update the
        # identity with the nodes that the user provides
        if hasattr(current_user, "roles"):
            for role in current_user.roles:
                for node in role.nodes:
                    if (node.status == 1) and (current_user.status == 1) and (role.status == 1):
                        identity.provides.add(ActionNeed(node.nodeName))
    except:
        pass


@aun_admin.route('/logout')
def logout():
    """ function docstring
    """
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    return redirect(request.args.get('next') or '/')


@aun_app.route("/templates/Admin/<string:path>", methods=['GET', "POST"])
def get_admin_html(path):
    """ function docstring
    """
    path = os.path.join(basedir, 'aunet/templates/admin/', path)
    try:
        with open(path, 'r', encoding='utf-8') as response:
            return response.read()
    except:
        return "not found", 404


@aun_app.route("/dashboard", methods=["GET"])
@aun_app.route("/dashboard/<path:path>", methods=["GET"])
def get_app(path=None):
    """ function docstring
    """
    path = os.path.join(basedir, 'aunet/templates/admin/app.html')
    with open(path, 'r', encoding='utf-8') as response:
        return response.read()


@aun_app.route("/api/templates/<path:path>", methods=["GET"])
def get_template(path):
    """
    Args: 
        path: the path of the template file needed. "admin/app.html"

    Return:
        return the template file
    """
    path = os.path.join(basedir, 'aunet/templates/', path)
    try:
        with open(path, 'r', encoding='utf-8') as response:
            return response.read()
    except:
        return "not found", 404

# User 模块
aun_api.add_resource(CurrentUserApi, "/api/user/current-user")
aun_api.add_resource(UsersApi, '/api/user/users')
aun_api.add_resource(UserApi, "/api/user/users/<string:id>")
aun_api.add_resource(NodesApi, "/api/user/nodes")
aun_api.add_resource(NodeApi, "/api/user/nodes/<string:id>")
aun_api.add_resource(RolesApi, "/api/user/roles")
aun_api.add_resource(RoleApi, "/api/user/roles/<string:id>")


# Article 模块
aun_api.add_resource(SlideshowsApi, "/api/news/slide-shows")
aun_api.add_resource(SlideshowApi, "/api/news/slider-shows/<string:id>")
aun_api.add_resource(ArticlesApi, "/api/news/news", endpoint="newses")
# gai
aun_api.add_resource(ArticleApi, "/api/news/news/<string:id>", endpoint="news")
aun_api.add_resource(
    ArticleDetailApi, "/api/news/news/<string:id>/detail")
aun_api.add_resource(TagsApi, "/api/article/tags")
aun_api.add_resource(TagApi, "/api/article/tags/<string:id>")
aun_api.add_resource(CategorysApi, "/api/article/categorys")
aun_api.add_resource(CategoryApi, "/api/article/categorys/<string:id>")

aun_api.add_resource(
    ArticlesApi, "/api/clubs/<string:club_id>/articles", endpoint="culb_articles")
aun_api.add_resource(
    ArticleApi, "/api/clubs/<string:club_id>/articles/<string:article_id>", endpoint="culb_article")


# Search 模块
aun_api.add_resource(SearchArticleApi, "/api/search/article")
aun_api.add_resource(LoginApi, "/api/login")
