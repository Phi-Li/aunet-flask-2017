# -*- coding: utf-8 -*-

""" admin for aun
"""

from flask import Blueprint, current_app

aun_admin = Blueprint('admin', __name__,)

from aun.admin import views
