# -*-coding:utf-8 -*-

""" module docstring
"""

# build restful api for user modoul

from datetime import datetime
import json

from flask_restful import reqparse, abort, Resource, fields, marshal_with
from flask_principal import RoleNeed, UserNeed, ActionNeed
from flask_principal import Identity, AnonymousIdentity, \
    identity_changed, Permission
from werkzeug.security import generate_password_hash
from flask_login import current_user
from flask import request, render_template

from aun.admin.models import User, Node, Role, LoginLog
from aun import aun_db
from .models import EditUserPermission, EditUserNeed, LoginLog
from .email import send_email

Node_fields = {
    "id": fields.Integer,
    "nodeName": fields.String,
    "status": fields.Boolean,
    "level": fields.Integer
}

# parser for Users
User_parser = reqparse.RequestParser()
User_parser.add_argument(
    'userName', type=str, required=True, location="json", help="userName is needed")
User_parser.add_argument(
    'passWord', type=str, required=True, location="json", help="passWord is needed")
User_parser.add_argument(
    'email', type=str, location="json", help="email is needed", required=True)
User_parser.add_argument(
    'phone', type=str, location="json", help="phone is needed", required=True)
User_parser.add_argument('roleName', type=str, required=True,
                         location="json", action="append", help="roleName is needed")

# parser for UserSpec
UserSpec_parser = reqparse.RequestParser()
UserSpec_parser.add_argument('email', type=str, location="json")
UserSpec_parser.add_argument('phone', type=str, location="json")
UserSpec_parser.add_argument('passWord', type=str, location="json")
UserSpec_parser.add_argument(
    'roleName', type=str, location="json", action="append")
UserSpec_parser.add_argument('userName', type=str, location="json")
UserSpec_parser.add_argument('status', type=bool, location="json")

# parser for NodeSpec
NodeSpec_parser = reqparse.RequestParser()
NodeSpec_parser.add_argument('status', type=int, help="status type is int")
NodeSpec_parser.add_argument('level', type=int, help="permission level")

# parser for Role
Role_parser = reqparse.RequestParser()
Role_parser.add_argument(
    'roleName', type=str, location="json", required=True, help="roleName is needed")
Role_parser.add_argument("nodeName", type=str, location="json",
                         action="append", required=True, help="remark is needed")
# parser for RoleSpec
RoleSpec_parser = reqparse.RequestParser()
RoleSpec_parser.add_argument('roleName', type=str, location="json")
RoleSpec_parser.add_argument(
    'nodeName', action="append", type=str, location="json")
RoleSpec_parser.add_argument('status', type=bool, location="json")


RequestMethod_parser = reqparse.RequestParser()
RequestMethod_parser.add_argument('requestMethod', type=str, location='json')


def abort_if_not_exist(data, message):
    """ function docstring
    """
    if data is None:
        abort(404, message="{}  Found".format(message))


def abort_if_exist(data, message):
    """ function docstring
    """
    if data != None:
        abort(
            400, message="{} has existed ,please try another".format(message))


def abort_if_unauthorized(message):
    """ function docstring
    """
    abort(401, message="{} permission Unauthorized".format(message))


def build_user_data(user):
    """ function docstring
    """
    log = LoginLog.query.filter(LoginLog.userName == user.userName).order_by(
        LoginLog.id.desc()).first()
    data = dict()
    if log != None:
        data['loginIp'] = log.loginIp
        data['loginTime'] = log.loginTime.timestamp()
    else:
        data['loginIp'] = None
        data['loginTime'] = None
    data['id'] = user.id
    data['userName'] = user.userName
    data['status'] = user.status
    data['email'] = user.email
    data['phone'] = user.phone
    data['roles'] = list()
    data['nodes'] = list()
    for role in user.roles:
        for node in role.nodes:
            n = dict()
            n['id'] = node.id
            n['nodeName'] = node.nodeName
            n['status'] = node.status
            n['level'] = node.level
            data['nodes'].append(n)
        r = dict()
        r['id'] = role.id
        r['roleName'] = role.role_name
        r['status'] = role.status
        data['roles'].append(r)

    return data


def build_role_data(role):
    """ function docstring
    """
    data = dict()
    data['id'] = role.id
    data['roleName'] = role.role_name
    data['status'] = role.status
    data['nodes'] = list()
    for node in role.nodes:
        n = dict()
        n['id'] = node.id
        n['nodeName'] = node.nodeName
        n['status'] = node.status
        n['level'] = node.level
        data['nodes'].append(n)

    return data


class Users(Resource):
    """ class docstring
    """

    def get(self):
        """ method docstring
        """
        permission = Permission(ActionNeed(('查看用户')))
        if permission.can() is not True:
            abort_if_unauthorized("查看用户")
        datas = list()
        users = User.query.all()
        for user in users:
            data = build_user_data(user)
            datas.append(data)
        return datas

    def post(self):
        """ method docstring
        """
        request_arg = RequestMethod_parser.parse_args()
        request_method = request_arg['requestMethod']
        if request_method == "POST":
            permission = Permission(ActionNeed('添加用户'))
            if permission.can()is not True:
                abort_if_unauthorized("添加用户")
            args = User_parser.parse_args()
            try:
                args['roleName'] = list(eval(args['roleName'][0]))
            except:
                pass
            user_name = args['userName']
            password = args['passWord']
            email = args['email']
            role_name = args['_n']
            phone = args['phone']
            user1 = User.query.filter(User.user_name == user_name).first()
            abort_if_exist(user1, "userName")
            try:
                html = render_template(
                    "Admin/user_info.html", user_name=user_name, password=password, flag="创建账号")
                send_email("社团网账号信息", [email], html)
                user = User(user_name, password, email, phone)
                for name in role_name:
                    role = Role.query.filter(Role.role_name == name).first()
                    abort_if_not_exist(role, "role")
                    user.roles.append(role)
                aun_db.session.add(user)
                aun_db.session.commit()
            except:
                pass
        else:
            abort(404, message="api not found")


class CurrentUser(Resource):
    """ class docstring
    """

    def get(self):
        """ method docstring
        """
        user = current_user
        abort_if_not_exist(user, "user")
        data = build_user_data(user)
        return data


class UserSpec(Resource):
    """ class docstring
    """

    def get(self, user_id):
        """ method docstring
        """
        user = User.query.filter(User.id == user_id).first()
        abort_if_not_exist(user, "user")
        data = build_user_data(user)
        return data

    def post(self, user_id):
        """ method docstring
        """
        request_arg = RequestMethod_parser.parse_args()
        request_method = request_arg['requestMethod']
        if request_method == "PUT":
            if current_user.is_anonymous is True:
                abort_if_unauthorized("修改用户")
            permission = Permission(ActionNeed("修改用户"))
            user = User.query.filter(User.id == user_id).first()
            abort_if_not_exist(user, "user")
            if user != current_user and permission.can() is not True:
                abort_if_unauthorized("修改用户")  # 用户默认能修改自己的信息
            args = UserSpec_parser.parse_args()
            # userId=args['userId']
            status = args['status']
            email = args['email']
            phone = args['phone']
            password = args['passWord']
            role_name = args['roleName']
            user_name = args['userName']
            if user_name != None and user_name != user.user_name:
                user1 = User.query.filter(User.user_name == user_name).first()
                abort_if_exist(user1, "userName")
                user.user_name = user_name

            if status != None and permission.can():
                user.status = status
            if email != None:
                user.email = email
            if phone != None:
                user.phone = phone
            if password != None:
                try:
                    html = render_template(
                        "Admin/user_info.html", user_name=user.userName, password=password, flag="修改密码")
                    send_email("社团网账号信息", [user.email], html)
                    user.password = generate_password_hash(password)
                except:
                    pass

            if role_name != None and permission.can():
                try:
                    role_name = list(eval(role_name[0]))
                except:
                    pass
                r = list()
                for name in role_name:
                    role = Role.query.filter(Role.role_name == name).first()
                    abort_if_not_exist(role, "role")
                    r.append(role)
                user.roles = r
            if user_name != None:
                user.userName = user_name
            aun_db.session.add(user)
            aun_db.session.commit()
        elif request_method == "DELETE":
            permission = Permission(ActionNeed("删除用户"))
            if permission.can()is not True:
                abort_if_unauthorized("删除用户")
            user = User.query.filter(User.id == id).first()
            abort_if_not_exist(user, "user")
            aun_db.session.delete(user)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class Nodes(Resource):
    """ class docstring
    """

    @marshal_with(Node_fields)
    def get(self):
        """ method docstring
        """
        permission = Permission(ActionNeed(('查看权限节点')))
        if permission.can() is not True:
            abort_if_unauthorized("查看权限节点")
        nodes = Node.query.all()
        return nodes


class NodeSpec(Resource):
    """ class docstring
    """

    @marshal_with(Node_fields)
    def get(self, node_id):
        """ method docstring
        """
        permission = Permission(ActionNeed(('查看权限节点')))
        if permission.can() is not True:
            abort_if_unauthorized("查看权限节点")
        node = Node.query.filter(Node.id == node_id).first()
        abort_if_not_exist(node, "node")
        return node

    def post(self, node_id):
        """ method docstring
        """
        request_arg = RequestMethod_parser.parse_args()
        request_method = request_arg['requestMethod']
        if request_method == "PUT":
            permission = Permission(ActionNeed("修改节点"))
            if permission.can()is not True:
                abort_if_unauthorized("修改节点")

            node = Node.query.filter(Node.id == node_id).first()
            abort_if_not_exist(node, "node")
            args = NodeSpec_parser.parse_args()
            status = args['status']
            level = args['level']
            if status != None:
                if node.nodeName != "修改节点":  # 不能禁用“修改节点”权限节点
                    node.status = status
            if level != None:
                node.level = level
            aun_db.session.add(node)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class Roles(Resource):
    """ class docstring
    """

    def get(self):
        """ method docstring
        """
        permission = Permission(ActionNeed(('查看角色')))
        if permission.can() is not True:
            abort_if_unauthorized("查看角色")
        roles = Role.query.all()
        datas = list()
        for role in roles:
            data = build_role_data(role)
            datas.append(data)
        return datas

    def post(self):
        """ method docstring
        """
        request_arg = RequestMethod_parser.parse_args()
        request_method = request_arg['requestMethod']
        print(request_method)
        if request_method == "POST":
            permission = Permission(ActionNeed('添加角色'))
            if permission.can()is not True:
                abort_if_unauthorized("添加角色")
            args = Role_parser.parse_args()
            role_name = args['roleName']
            try:
                node_name = list(eval(args['nodeName'][0]))
            except:
                node_name = args['nodeName']

            role1 = Role.query.filter(Role.role_name == role_name).first()
            abort_if_exist(role1, "roleName")
            role = Role(role_name)
            aun_db.session.add(role)
            aun_db.session.commit()
            for name in node_name:
                node = Node.query.filter(Node.node_name == name).first()
                abort_if_not_exist(node, "node")
                role.nodes.append(node)
            aun_db.session.add(role)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class RoleSpec(Resource):
    """ method docstring
    """

    def get(self, role_id):
        """ method docstring
        """
        permission = Permission(ActionNeed(('查看角色')))
        if permission.can() is not True:
            abort_if_unauthorized("查看角色")
        role = Role.query.filter(Role.id == role_id).first()
        abort_if_not_exist(role, "role")
        data = build_role_data(role)
        return data

    def post(self, role_id):
        """ method docstring
        """
        request_arg = RequestMethod_parser.parse_args()
        request_method = request_arg['requestMethod']
        if request_method == "PUT":
            permission = Permission(ActionNeed('修改角色'))
            if permission.can()is not True:
                abort_if_unauthorized("修改角色")

            role = Role.query.filter(Role.id == role_id).first()
            abort_if_not_exist(role, "role")
            args = RoleSpec_parser.parse_args()
            role_name = args['roleName']
            node_name = args['nodeName']
            status = args['status']
            if role_name != None and role_name != role.role_name:
                r = Role.query.filter_by(roleName=role_name).first()
                abort_if_exist(r, "rolename")
                role.role_name = role_name
            if status != None:
                if role.rolename != "超管":  # 不能禁用超管角色
                    role.status = status
            if node_name != None:
                try:
                    node_name = list(eval(node_name[0]))
                except:
                    pass
                n = list()
                for name in node_name:
                    node = Node.query.filter(Node.node_name == name).first()
                    abort_if_not_exist(node, "node")
                    n.append(node)
                role.nodes = n

            aun_db.session.add(role)
            aun_db.session.commit()
        elif request_method == "DELETE":
            permission = Permission(ActionNeed('删除角色'))
            if permission.can()is not True:
                abort_if_unauthorized("删除角色")

            role = Role.query.filter(Role.id == id).first()
            abort_if_not_exist(role, "role")
            aun_db.session.delete(role)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")
