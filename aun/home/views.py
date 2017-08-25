# -*-coding:utf-8 -*-

""" module docstring
"""


from flask import render_template, request

from aun.home import home
from aun.home.models import Article, Category, SlideShow, article_category


@home.route('/', methods=["POST", "GET"])
@home.route('/index', methods=["POST", "GET"])
def index():
    """ 
    index page
    """
    return render_template("home/index.html")


@home.route('/news', methods=["POST", "GET"])
def index_article():
    """ 
    news page
    """
    return render_template("home/news/index.html")
