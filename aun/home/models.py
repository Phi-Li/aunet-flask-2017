# -*-coding:utf-8 -*-

""" module docstring
"""

from datetime import datetime
from flask_login import current_user
from .. import aun_db


news_category = aun_db.Table("news_category",
                             aun_db.Column(
                                 'news_id', aun_db.Integer, aun_db.ForeignKey("news.id")),
                             aun_db.Column(
                                 'category_id', aun_db.Integer, aun_db.ForeignKey("category.id")),
                             aun_db.Column(
                                 "created_at", aun_db.DateTime, default=datetime.now)
                            )

news_tag = aun_db.Table("news_tag",
                        aun_db.Column(
                            "news_id", aun_db.Integer, aun_db.ForeignKey("news.id")),
                        aun_db.Column(
                            "tag_id", aun_db.Integer, aun_db.ForeignKey("tag.id")),
                        aun_db.Column(
                            "created_at", aun_db.DateTime, default=datetime.now),
                       )


class News(aun_db.Model):
    """ class docstring
    """
    __tablename__ = "news"
    news_id = aun_db.Column(aun_db.Integer, primary_key=True)
    year = aun_db.Column(aun_db.Integer)
    month = aun_db.Column(aun_db.Integer)
    day = aun_db.Column(aun_db.Integer)
    post_time = aun_db.Column(aun_db.DateTime)
    detail = aun_db.Column(aun_db.Text)
    title = aun_db.Column(aun_db.String(80))
    outline = aun_db.Column(aun_db.Text)
    img_url = aun_db.Column(aun_db.String(50))
    editable = aun_db.Column(aun_db.Boolean)
    author = aun_db.Column(aun_db.String(40))
    category = aun_db.relationship(
        "Category", secondary=news_category, backref=aun_db.backref('news', lazy="dynamic"))
    tags = aun_db.relationship(
        "Tag", secondary=news_tag, backref=aun_db.backref('news', lazy="dynamic"))

    def add_category(self, category_name):
        """ method docstring
        """
        category = Category.query.filter(Category.name == category_name).first()
        self.category.append(category)

    def add_tag(self, tag_name):
        """ method docstring
        """
        tag = Tag.query.filter(Tag.name == tag_name).first()
        self.tags.append(tag)

    @property
    def cate(self):
        """ method docstring
        """
        return self.category[0].name

    def __init__(self, news_detail, news_title, news_outline, news_img_url):
        time = datetime.utcnow()
        self.post_time = time
        self.year = time.year
        self.month = time.month
        self.day = time.day
        self.detail = news_detail
        self.title = news_title
        self.outline = news_outline
        self.img_url = news_img_url
        self.editable = True
        if current_user is None:
            self.author = "匿名"
        else:
            self.author = current_user.userName

    def __str__(self):
        return "Title:%s" % self.title
    __repr__ = __str__


class Category(aun_db.Model):
    """ class docstring
    """
    __tablename__ = "category"
    cat_id = aun_db.Column(aun_db.Integer, primary_key=True)
    name = aun_db.Column(aun_db.String(30), unique=True)
    remark = aun_db.Column(aun_db.String(30))

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "category_name:%s" % self.name
    __repr__ = __str__


class Tag(aun_db.Model):
    """ class docstring
    """
    __tablename__ = "tag"
    tag_id = aun_db.Column(aun_db.Integer, primary_key=True)
    name = aun_db.Column(aun_db.String(30), unique=True)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "tag_name:%s" % self.name

    __repr__ = __str__


class SilderShow(aun_db.Model):
    """ class docstring
    """
    slide_id = aun_db.Column(aun_db.Integer, primary_key=True)
    title = aun_db.Column(aun_db.String(80))
    img_url = aun_db.Column(aun_db.String(80))
    outline = aun_db.Column(aun_db.Text)
    post_time = aun_db.Column(aun_db.DateTime)
    link = aun_db.Column(aun_db.String(80))
    editable = aun_db.Column(aun_db.Boolean)

    def __init__(self, title, url, outline, link):
        self.title = title
        self.img_url = url
        self.outline = outline
        self.link = link
        self.editable = 1
        self.post_time = datetime.utcnow()

    def __str__(self):
        return self.title
    __repr__ = __str__
