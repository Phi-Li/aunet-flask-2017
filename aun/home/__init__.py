# -*- coding: utf-8 -*-
""" module docstring
"""
from flask import Blueprint

home = Blueprint('home', __name__)

from aun.home import views, models
