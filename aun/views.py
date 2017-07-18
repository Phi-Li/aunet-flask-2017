# -*-coding:utf-8 -*-

""" route definition
"""

from flask import render_template
from aun import aun_app


@aun_app.route('/developing')
def develop_next():
    """ page developing
    """
    return render_template('Public/fixed.html')
