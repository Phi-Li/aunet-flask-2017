# -*- coding: utf-8 -*-

""" admin for aun
"""

from flask import Blueprint
from itsdangerous import URLSafeTimedSerializer
from aun import aun_app
from . import views

aun_admin = Blueprint('admin', __name__,)
serializer = URLSafeTimedSerializer(aun_app.config['SECRET_KEY'])
