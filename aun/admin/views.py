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
from aun.admin.news import SlideshowClass, SlideshowSpec, NewsClass, NewsSpec, NewsSpecDetail, Tags, TagClass, Categorys, CategoryClass
from aun.admin.users import Users, UserSpec, Roles, RoleSpec, Nodes, NodeSpec, CurrentUser
from aun.admin.search import SearchNews
from aun.admin.login import Login
from aun.admin.models import User
from aun.admin.models import EditUserPermission

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
        # user has the permission of edit himself

        identity.provides.add(EditUserPermission(current_user.id))

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
aun_api.add_resource(CurrentUser, "/api/user/current-user")
aun_api.add_resource(Users, '/api/user/users')
aun_api.add_resource(UserSpec, "/api/user/users/<string:id>")
aun_api.add_resource(Nodes, "/api/user/nodes")
aun_api.add_resource(NodeSpec, "/api/user/nodes/<string:id>")
aun_api.add_resource(Roles, "/api/user/roles")
aun_api.add_resource(RoleSpec, "/api/user/roles/<string:id>")


# News 模块
aun_api.add_resource(SlideshowClass, "/api/sews/slide-show")
aun_api.add_resource(SlideshowSpec, "/api/news/slider-show/<string:id>")
aun_api.add_resource(NewsClass, "/api/news/news")
aun_api.add_resource(NewsSpec, "/api/news/news/<string:id>")  # gai
aun_api.add_resource(NewsSpecDetail, "/api/news/news/<string:id>/Detail")
aun_api.add_resource(Tags, "/api/news/tags")
aun_api.add_resource(TagClass, "/api/news/tags/<string:id>")
aun_api.add_resource(Categorys, "/api/news/categorys")
aun_api.add_resource(CategoryClass, "/api/news/categorys/<string:id>")

# Search 模块
aun_api.add_resource(SearchNews, "/api/search/news")
aun_api.add_resource(Login, "/api/login")
