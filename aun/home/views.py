# -*-coding:utf-8 -*-

""" 
home 
"""


from flask import render_template, request, current_app
import os

from aun.home import home
from aun.home.models import Article, Category, SlideShow, article_category


@home.route("/", methods=["GET"])
@home.route("/<path:path>", methods=["GET"])
def get_app(path=None):
    """ 
    get index page
    """
    basedir = current_app.config['BASEDIR']
    path = os.path.join(basedir, 'aun/templates/home/index.html')
    with open(path, 'r', encoding='utf-8') as response:
        return response.read()
