# -*-coding:utf-8 -*-

""" user related table
"""

from collections import namedtuple
from functools import partial
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_principal import Permission

from aun import aun_db
from aun.association.models import Club

role_node = aun_db.Table('role_node',  # 角色权限关联表
                         aun_db.Column(
                             'node_id', aun_db.Integer, aun_db.ForeignKey('node.node_id')),
                         aun_db.Column(
                             'role_id', aun_db.Integer, aun_db.ForeignKey('role.role_id')),
                         aun_db.Column(
                             'created_at', aun_db.DateTime, default=datetime.now)
                         )

user_role = aun_db.Table('user_role',  # 用户角色关联表
                         aun_db.Column(
                             'user_id', aun_db.Integer, aun_db.ForeignKey('user.user_id')),
                         aun_db.Column(
                             'role_id', aun_db.Integer, aun_db.ForeignKey('role.role_id')),
                         aun_db.Column(
                             'created_at', aun_db.DateTime, default=datetime.now)
                         )

user_club = aun_db.Table('user_club',
                         aun_db.Column(
                             'user_id', aun_db.Integer, aun_db.ForeignKey('user.user_id')),
                         aun_db.Column('club_id', aun_db.Integer,
                                       aun_db.ForeignKey('club.club_id')),
                         aun_db.Column(
                             "created_at", aun_db.DateTime, default=datetime.now)
                         )

EditUserNeed = partial(namedtuple('User', ['method', 'value']), 'edit')


class LoginLog(aun_db.Model):
    """ login log 
    """
    log_id = aun_db.Column(aun_db.Integer, primary_key=True)
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
    """ node table
    """
    __tablename__ = "node"
    node_id = aun_db.Column(aun_db.Integer, primary_key=True)
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
    role_id = aun_db.Column(aun_db.Integer, primary_key=True)
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
    """ User table
    """
    __tablename__ = "user"
    user_id = aun_db.Column(aun_db.Integer, primary_key=True)
    user_name = aun_db.Column(aun_db.String(64), unique=True, index=True)
    password = aun_db.Column(aun_db.String(128))
    email = aun_db.Column(aun_db.String(40))
    status = aun_db.Column(aun_db.Boolean)
    remark = aun_db.Column(aun_db.String(20))
    phone = aun_db.Column(aun_db.String(20))

    clubs = aun_db.relationship(
        "Club", secondary=user_club, backref=aun_db.backref("users", lazy="dynamic"))
    roles = aun_db.relationship(
        "Role", secondary=user_role, backref=aun_db.backref('users', lazy="dynamic"))

    def verify_password(self, password):
        """ verify password
        """
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.user_id

    @property
    def nodes(self):
        """ 
        Return
            user's all permission node
        """
        node = []
        for r in self.role:
            node = node + r.nodes
        return node

    def add_role(self, role_name):
        """ add a role for user
        """
        r = Role.query.filter(Role.role_name == role_name).first()
        self.roles.append(r)

    def add_club(self, name):
        """
        each user can handle many club
        add a club to user accocount 
        """
        club = club.query.filter(
            club.name == name).first()
        self.clubs.append(club)

    def __init__(self, user_name, password, email, phone):
        self.user_name = user_name
        self.password = generate_password_hash(password)
        self.email = email
        self.status = True
        self.phone = phone

    def __str__(self):
        return self.user_name

    __repr__ = __str__
