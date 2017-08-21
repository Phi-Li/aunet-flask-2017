# -*- coding: utf-8 -*-

""" association related table
"""
from datetime import datetime
from aun import aun_db
from aun.home.models import Article

association_article = aun_db.Table('association_article',  # 角色权限关联表
                                   aun_db.Column(
                                       'association_id', aun_db.Integer, aun_db.ForeignKey('Association.association_id')),
                                   aun_db.Column(
                                       'article_id', aun_db.Integer, aun_db.ForeignKey('Article.article_id')),
                                   aun_db.Column(
                                       'created_at', aun_db.DateTime, default=datetime.now)
                                   )


class Association(aun_db.Model):
    """
    association table
    """
    __tablename__ = "association"
    association_id = aun_db.Column(aun_db.Integer, primary_key=True)
    name = aun_db.Column(aun_db.String(30), unique=True)
    brief_introduction = aun_db.Column(
        aun_db.Text)  # used in association space
    detailed_introduction = aun_db.Column(
        aun_db.Text)  # used in association union page
    category = aun_db.Column(aun_db.String(20))
    picture = aun_db.Column(aun_db.String(30))
    articles = aun_db.relationship(
        "Article", secondary=association_article, backref=aun_db.backref('association', lazy="dynamic"))
    # if Article.association == [] then this article is Association article

    def __init__(self, name, instrodiction, category, picture):
        self.name = name,
        self.instrodiction = instrodiction
        self.picture = picture
        self.category = category

    def add_article(self, article):
        """
        Args:
                article : a instance of Article
        """
        self.articles.append(article)

    def __str__(self):
        return "association name:%s" % self.name
    __repr__ = __str__
