# -*-coding:utf-8 -*-

""" rest api for user related
"""

# build restful api for user modoul
from flask_restful import reqparse, abort, Resource, fields, marshal_with
from flask_principal import ActionNeed
from flask_principal import Permission
from werkzeug.security import generate_password_hash
from flask_login import current_user
from flask import render_template

from aun.admin.models import User, Node, Role, LoginLog
from aun import aun_db
from aun.admin.email import send_email
from aun.common import abort_if_exist, abort_if_not_exist, abort_if_unauthorized

node_fields = {
    "id": fields.Integer,
    "node_name": fields.String,
    "status": fields.Boolean,
    "level": fields.Integer
}

# parser for Users
user_parser = reqparse.RequestParser()
user_parser.add_argument(
    'user_name', type=str, required=True, location="json", help="user_name is needed")
user_parser.add_argument(
    'password', type=str, required=True, location="json", help="password is needed")
user_parser.add_argument(
    'email', type=str, location="json", help="email is needed", required=True)
user_parser.add_argument(
    'phone', type=str, location="json", help="phone is needed", required=True)
user_parser.add_argument('role_name', type=str, required=True,
                         location="json", action="append", help="role_name is needed")

# parser for UserSpec
user_spec_parser = reqparse.RequestParser()
user_spec_parser.add_argument('email', type=str, location="json")
user_spec_parser.add_argument('phone', type=str, location="json")
user_spec_parser.add_argument('password', type=str, location="json")
user_spec_parser.add_argument(
    'role_name', type=str, location="json", action="append")
user_spec_parser.add_argument('user_name', type=str, location="json")
user_spec_parser.add_argument('status', type=bool, location="json")

# parser for NodeSpec
node_spec_parser = reqparse.RequestParser()
node_spec_parser.add_argument('status', type=int, help="status type is int")
node_spec_parser.add_argument('level', type=int, help="permission level")

# parser for Role
role_parser = reqparse.RequestParser()
role_parser.add_argument(
    'role_name', type=str, location="json", required=True, help="role_name is needed")
role_parser.add_argument("node_name", type=str, location="json",
                         action="append", required=True, help="remark is needed")
# parser for RoleSpec
role_spec_parser = reqparse.RequestParser()
role_spec_parser.add_argument('role_name', type=str, location="json")
role_spec_parser.add_argument(
    'node_name', action="append", type=str, location="json")
role_spec_parser.add_argument('status', type=bool, location="json")


request_method_parser = reqparse.RequestParser()
request_method_parser.add_argument('request_method', type=str, location='json')


def build_user_data(user):
    """ function docstring
    """
    log = LoginLog.query.filter(LoginLog.user_name == user.user_name).order_by(
        LoginLog.id.desc()).first()
    data = dict()
    if log != None:
        data['loginIp'] = log.loginIp
        data['loginTime'] = log.loginTime.timestamp()
    else:
        data['loginIp'] = None
        data['loginTime'] = None
    data['id'] = user.user_id
    data['user_name'] = user.user_name
    data['status'] = user.status
    data['email'] = user.email
    data['phone'] = user.phone
    data['roles'] = list()
    data['nodes'] = list()
    for role in user.roles:
        for node in role.nodes:
            n = dict()
            n['id'] = node.node_id
            n['node_name'] = node.node_name
            n['status'] = node.status
            n['level'] = node.level
            data['nodes'].append(n)
        r = dict()
        r['id'] = role.role_id
        r['role_name'] = role.role_name
        r['status'] = role.status
        data['roles'].append(r)

    return data


def build_role_data(role):
    """ function docstring
    """
    data = dict()
    data['id'] = role.role_id
    data['role_name'] = role.role_name
    data['status'] = role.status
    data['nodes'] = list()
    for node in role.nodes:
        n = dict()
        n['id'] = node.node_id
        n['node_name'] = node.node_name
        n['status'] = node.status
        n['level'] = node.level
        data['nodes'].append(n)

    return data


class UsersApi(Resource):
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
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "POST":
            permission = Permission(ActionNeed('添加用户'))
            if permission.can()is not True:
                abort_if_unauthorized("添加用户")
            args = user_parser.parse_args()
            try:
                args['role_name'] = list(eval(args['role_name'][0]))
            except:
                pass
            user_name = args['user_name']
            password = args['password']
            email = args['email']
            role_name = args['_n']
            phone = args['phone']
            user1 = User.query.filter(User.user_name == user_name).first()
            abort_if_exist(user1, "user_name")
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


class CurrentUserApi(Resource):
    """ class docstring
    """

    def get(self):
        """ method docstring
        """
        user = current_user
        abort_if_not_exist(user, "user")
        data = build_user_data(user)
        return data


class UserApi(Resource):
    """ class docstring
    """

    def get(self, user_id):
        """ method docstring
        """
        user = User.query.filter(User.user_id == user_id).first()
        abort_if_not_exist(user, "user")
        data = build_user_data(user)
        return data

    def post(self, user_id):
        """ method docstring
        """
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "PUT":
            if current_user.is_anonymous is True:
                abort_if_unauthorized("修改用户")
            permission = Permission(ActionNeed("修改用户"))
            user = User.query.filter(User.user_id == user_id).first()
            abort_if_not_exist(user, "user")
            if user != current_user and permission.can() is not True:
                abort_if_unauthorized("修改用户")  # 用户默认能修改自己的信息
            args = user_spec_parser.parse_args()
            # userId=args['userId']
            status = args['status']
            email = args['email']
            phone = args['phone']
            password = args['password']
            role_name = args['role_name']
            user_name = args['user_name']
            if user_name != None and user_name != user.user_name:
                user1 = User.query.filter(User.user_name == user_name).first()
                abort_if_exist(user1, "user_name")
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
                        "Admin/user_info.html", user_name=user.user_name, password=password, flag="修改密码")
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
                user.user_name = user_name
            aun_db.session.add(user)
            aun_db.session.commit()
        elif request_method == "DELETE":
            permission = Permission(ActionNeed("删除用户"))
            if permission.can()is not True:
                abort_if_unauthorized("删除用户")
            user = User.query.filter(User.user_id == user_id).first()
            abort_if_not_exist(user, "user")
            aun_db.session.delete(user)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class NodesApi(Resource):
    """ class docstring
    """

    @marshal_with(node_fields)
    def get(self):
        """ method docstring
        """
        permission = Permission(ActionNeed(('查看权限节点')))
        if permission.can() is not True:
            abort_if_unauthorized("查看权限节点")
        nodes = Node.query.all()
        return nodes


class NodeApi(Resource):
    """ class docstring
    """

    @marshal_with(node_fields)
    def get(self, node_id):
        """ method docstring
        """
        permission = Permission(ActionNeed(('查看权限节点')))
        if permission.can() is not True:
            abort_if_unauthorized("查看权限节点")
        node = Node.query.filter(Node.node_id == node_id).first()
        abort_if_not_exist(node, "node")
        return node

    def post(self, node_id):
        """ method docstring
        """
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "PUT":
            permission = Permission(ActionNeed("修改节点"))
            if permission.can()is not True:
                abort_if_unauthorized("修改节点")

            node = Node.query.filter(Node.id == node_id).first()
            abort_if_not_exist(node, "node")
            args = node_spec_parser.parse_args()
            status = args['status']
            level = args['level']
            if status != None:
                if node.node_name != "修改节点":  # 不能禁用“修改节点”权限节点
                    node.status = status
            if level != None:
                node.level = level
            aun_db.session.add(node)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class RolesApi(Resource):
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
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        print(request_method)
        if request_method == "POST":
            permission = Permission(ActionNeed('添加角色'))
            if permission.can()is not True:
                abort_if_unauthorized("添加角色")
            args = role_parser.parse_args()
            role_name = args['role_name']
            try:
                node_name = list(eval(args['node_name'][0]))
            except:
                node_name = args['node_name']

            role1 = Role.query.filter(Role.role_name == role_name).first()
            abort_if_exist(role1, "role_name")
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


class RoleApi(Resource):
    """ method docstring
    """

    def get(self, role_id):
        """ method docstring
        """
        permission = Permission(ActionNeed(('查看角色')))
        if permission.can() is not True:
            abort_if_unauthorized("查看角色")
        role = Role.query.filter(Role.role_id == role_id).first()
        abort_if_not_exist(role, "role")
        data = build_role_data(role)
        return data

    def post(self, role_id):
        """ method docstring
        """
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "PUT":
            permission = Permission(ActionNeed('修改角色'))
            if permission.can()is not True:
                abort_if_unauthorized("修改角色")

            role = Role.query.filter(Role.role_id == role_id).first()
            abort_if_not_exist(role, "role")
            args = role_spec_parser.parse_args()
            role_name = args['role_name']
            node_name = args['node_name']
            status = args['status']
            if role_name != None and role_name != role.role_name:
                r = Role.query.filter_by(role_name=role_name).first()
                abort_if_exist(r, "role_name")
                role.role_name = role_name
            if status != None:
                if role.role_name != "超管":  # 不能禁用超管角色
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

            role = Role.query.filter(Role.role_id == role_id).first()
            abort_if_not_exist(role, "role")
            aun_db.session.delete(role)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")
