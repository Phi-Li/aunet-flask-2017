# -*- coding: utf-8 -*-
""" module docstring
"""
from flask import Blueprint
from . import views, forms, models

home = Blueprint('home', __name__)
