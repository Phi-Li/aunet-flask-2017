# -*-coding:utf-8 -*-

""" route definition
"""

from flask import render_template
from aun.home import home


@home.route('/developing')
def develop_next():
    """ page developing
    """
    return render_template('public/fixed.html')


@home.route('/<path:path>')
def index_test(path):
    """

    """
    basedir = current_app.config['BASEDIR']
    path = os.path.join(basedir, 'aunet/templates/home/index.html')
    with open(path, 'r', encoding='utf-8') as response:
        return response.read()
