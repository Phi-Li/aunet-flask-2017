# -*-coding:utf-8 -*-

""" route definition
"""

from flask import render_template
from aun.home import home


@home.route('/developing')
def develop_next():
    """ page developing
    """
    return render_template('Public/fixed.html')
