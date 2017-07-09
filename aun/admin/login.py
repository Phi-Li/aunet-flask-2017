# -*-coding:utf-8 -*-

""" login module docstring
"""

from flask import request, current_app, session
from flask_login import login_user, current_user, logout_user
from flask_principal import identity_loaded, RoleNeed, UserNeed, ActionNeed
from flask_principal import Identity, AnonymousIdentity, \
    identity_changed, Permission
from flask_restful import reqparse, abort, Resource, fields, marshal_with

from aun import aun_app, aun_db

from .models import User, LoginLog
from .models import EditUserPermission, EditUserNeed
from .users import build_user_data


# Request parsers

login_parser = reqparse.RequestParser()
login_parser.add_argument('userName', type=str, location="json", required=True)
login_parser.add_argument('password', type=str, location="json", required=True)

request_method_parser = reqparse.RequestParser()
request_method_parser.add_argument('requestMethod', type=str, location='json')


@identity_loaded.connect_via(aun_app)
def on_identity_loaded(sender, identity):
    """ function docstring
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


def abort_if_unauthorized(message):
    """ function docstring
    """
    abort(401, message="{} permission Unauthorized".format(message))


class Login(Resource):
    """ class docstring
    """

    def get(self):
        """ method docstring
        """
        user = current_user
        if user.is_anonymous is True:
            abort(401, message="unlogined")
        if user.is_authenticated is not True:
            abort(401, message="unlogined")
        if user.is_active is not True:
            abort(401, message="unlogined")
        data = build_user_data(user)
        return data

    def post(self):
        """ method docstring
        """
        request_args = request_method_parser.parse_args()
        requestMethod = request_args['requestMethod']
        if requestMethod == "POST":
            login_args = login_parser.parse_args()
            userName = login_args['userName']
            password = login_args['password']
            user = User.query.filter(User.userName == userName).first()
            if user == None:
                abort(401, message="userName error")
            elif user.verify_password(password) is not True:
                abort(401, message="password error")
            else:
                session.permanent = True
                login_user(user)
                ip = str(request.remote_addr)
                log = LoginLog(current_user.userName, ip)
                aun_db.session.add(log)
                aun_db.session.commit()
                identity_changed.send(
                    current_app._get_current_object(), identity=Identity(user.id))
        elif requestMethod == "DELETE":
            # Remove the user information from the session
            logout_user()
            for key in ('identity.name', 'identity.auth_type'):
                session.pop(key, None)
        else:
            abort(404, message="api not found")
