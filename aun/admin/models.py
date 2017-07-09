# -*-coding:utf-8 -*-

""" module docstring
"""

from collections import namedtuple
from functools import partial
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_principal import Permission

from .. import aun_login, aun_db


role_node = aun_db.Table('role_node',  # 角色权限关联表
                         aun_db.Column(
                             'node_id', aun_db.Integer, aun_db.ForeignKey('node.id')),
                         aun_db.Column(
                             'role_id', aun_db.Integer, aun_db.ForeignKey('role.id')),
                         aun_db.Column('created_at', aun_db.DateTime, default=datetime.now)
                        )

user_role = aun_db.Table('user_role',  # 用户角色关联表
                         aun_db.Column(
                             'user_id', aun_db.Integer, aun_db.ForeignKey('user.id')),
                         aun_db.Column(
                             'role_id', aun_db.Integer, aun_db.ForeignKey('role.id')),
                         aun_db.Column('created_at', aun_db.DateTime, default=datetime.now)
                        )

EditUserNeed = partial(namedtuple('User', ['method', 'value']), 'edit')

class EditUserPermission(Permission):
    """ class docstring
    """

    def __init__(self, user_id):
        super(EditUserPermission, self).__init__(EditUserNeed(user_id))


class LoginLog(aun_db.Model):
    """ class docstring
    """
    user_id = aun_db.Column(aun_db.Integer, primary_key=True)
    user_name = aun_db.Column(aun_db.String(64))
    login_time = aun_db.Column(aun_db.DateTime)
    login_ip = aun_db.Column(aun_db.String(40))

    def __init__(self, user_name, login_ip):
        self.user_name = user_name
        self.login_time = datetime.utcnow()
        self.login_ip = login_ip

    def __str__(self):
        return self.user_name
    __repr__ = __str__


class Node(aun_db.Model):
    """ class docstring
    """
    __tablename__ = "node"
    user_id = aun_db.Column(aun_db.Integer, primary_key=True)
    node_name = aun_db.Column(aun_db.String(30), unique=True)
    remark = aun_db.Column(aun_db.String(30))
    status = aun_db.Column(aun_db.Boolean)
    level = aun_db.Column(aun_db.Integer)

    def __init__(self, node_name, level):
        self.node_name = node_name
        self.status = 1
        self.level = level

    def __str__(self):
        return self.node_name

    __repr__ = __str__


class Role(aun_db.Model):
    """ class docstring
    """
    __tablename__ = "role"
    user_id = aun_db.Column(aun_db.Integer, primary_key=True)
    role_name = aun_db.Column(aun_db.String(30), unique=True)
    status = aun_db.Column(aun_db.Boolean)
    remark = aun_db.Column(aun_db.String(30))

    nodes = aun_db.relationship(
        "Node", secondary=role_node, backref=aun_db.backref('roles', lazy="dynamic"))

    def add_node(self, node_name):
        """ method docstring
        """
        n = Node.query.filter(Node.node_name == node_name).first()
        self.nodes.append(n)

    def __init__(self, role_name):
        self.role_name = role_name
        self.status = 1

    def __str__(self):
        return self.role_name

    __repr__ = __str__


class User(aun_db.Model, UserMixin):
    """ class docstring
    """
    __tablename__ = "user"
    user_id = aun_db.Column(aun_db.Integer, primary_key=True)
    user_name = aun_db.Column(aun_db.String(64), unique=True, index=True)
    password = aun_db.Column(aun_db.String(128))
    email = aun_db.Column(aun_db.String(40))
    status = aun_db.Column(aun_db.Boolean)
    remark = aun_db.Column(aun_db.String(20))
    phone = aun_db.Column(aun_db.String(20))

    roles = aun_db.relationship(
        "Role", secondary=user_role, backref=aun_db.backref('users', lazy="dynamic"))

    def verify_password(self, password):
        """ method docstring
        """
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.user_id

    @property
    def nodes(self):
        """ method docstring
        """
        node = []
        for r in self.role:
            node = node + r.nodes
        return node

    def add_role(self, role_name):
        """ method docstring
        """
        r = Role.query.filter(Role.role_name == role_name).first()
        self.roles.append(r)

    def __init__(self, user_name, password, email, phone):
        self.user_name = user_name
        self.password = generate_password_hash(password)
        self.email = email
        self.status = True
        self.phone = phone

    def __str__(self):
        return self.user_name

    __repr__ = __str__
