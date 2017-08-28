# -*- coding: utf-8 -*-

""" club related table
"""
from datetime import datetime
from aun import aun_db
from aun.home.models import Article

club_article = aun_db.Table('club_article',  # 角色权限关联表
                            aun_db.Column(
                                'club_id', aun_db.Integer, aun_db.ForeignKey('club.club_id')),
                            aun_db.Column(
                                'article_id', aun_db.Integer, aun_db.ForeignKey('article.article_id')),
                            aun_db.Column(
                                'created_at', aun_db.DateTime, default=datetime.now)
                            )


class Club(aun_db.Model):
    """
    club table
    """
    __tablename__ = "club"
    club_id = aun_db.Column(aun_db.Integer, primary_key=True)
    name = aun_db.Column(aun_db.String(30), unique=True)
    brief_introduction = aun_db.Column(aun_db.Text)  # used in club space
    detailed_introduction = aun_db.Column(
        aun_db.Text)  # used in club union page
    category = aun_db.Column(aun_db.String(20))
    picture = aun_db.Column(aun_db.String(30))
    articles = aun_db.relationship(
        "Article", secondary=club_article, backref=aun_db.backref('club', lazy="dynamic"))
    # if Article.club == [] then this article is Club article

    def __init__(self, name, brief_introduction, category, picture):
        self.name = name
        self.brief_introduction = brief_introduction
        self.category = category
        self.picture = picture

    def add_article(self, article):
        """
        Args:
                article : a instance of Article
        """
        self.articles.append(article)

    def __str__(self):
        return "club name:%s" % self.name
    __repr__ = __str__
