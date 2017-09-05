# -*-coding:utf-8 -*-

""" manage article
"""
import time
import random
from io import BytesIO
from urllib import request
import os
import base64
from bs4 import BeautifulSoup
from PIL import Image
import json

from flask_restful import reqparse, abort, Resource, fields, marshal_with
from flask_principal import Permission, ActionNeed
from flask_login import current_user
from flask import current_app
# import models needed
from aun import aun_db
from aun.home.models import Article, SlideShow, Category, Tag
from aun.association.models import Club
from aun.common import abort_if_exist, abort_if_not_exist, abort_if_unauthorized, handle_html, dataurl_to_img


# Request parser for slideshow
slideshow_parser = reqparse.RequestParser()
slideshow_parser.add_argument(
    'title', type=str, required=True, location="json", help="title is needed")
slideshow_parser.add_argument(
    'img_url', type=str, required=True, location="json", help="imgUrl is needed")
slideshow_parser.add_argument(
    "outline", type=str, required=True, location="json", help="outline is needed")
slideshow_parser.add_argument(
    "link", type=str, required=True, location="json", help="the link that jump")


slideshow_spec_parser = reqparse.RequestParser()
slideshow_spec_parser.add_argument(
    'title', type=str, location="json", help="title")
slideshow_spec_parser.add_argument(
    'img_url', type=str, location="json", help="imgUrl")
slideshow_spec_parser.add_argument(
    "outline", type=str, location="json", help="outline")
slideshow_spec_parser.add_argument(
    "status", type=int, location='json', help="status")
slideshow_spec_parser.add_argument(
    "link", type=str, location="json", help="the link that jump")

# Request parser for article
article_parser = reqparse.RequestParser()
article_parser.add_argument(
    "category", type=str, location="json", required=True, help="category  is needed")
article_parser.add_argument(
    "detail", type=str, location="json", required=True, help="detail is needed")
article_parser.add_argument(
    "title", type=str, location="json", required=True, help="title is needed")
article_parser.add_argument("tags", type=str, location="json",
                            required=True, action='append', help="tags  is needed")

article_spec_parser = reqparse.RequestParser()
article_spec_parser.add_argument(
    "category", type=str, location="json", help="category")
article_spec_parser.add_argument(
    "detail", type=str, location="json", help="detail")
article_spec_parser.add_argument(
    "title", type=str, location="json", help="title")
article_spec_parser.add_argument(
    "status", type=int, location="json", help="edit status")
article_spec_parser.add_argument(
    "tags", type=str, location="json", action='append', help="tags id is needed")
article_spec_parser.add_argument('detail', type=str, location="json")


# Request parser for slideshow
parser = reqparse.RequestParser()
parser.add_argument(
    'name', type=str, location='json', help="name is needed", required=True)

parser_spec = reqparse.RequestParser()
parser_spec.add_argument('name', type=str, location='json')

# parser to judge DELETE or POST or PUT http method
request_method_parser = reqparse.RequestParser()
request_method_parser.add_argument('request_method', type=str, location='json')

# paging
paging_parser = reqparse.RequestParser()
paging_parser.add_argument("limit", type=int, location="args", required=True)
paging_parser.add_argument("offset", type=int, location="args", required=True)


class CategoryItem(fields.Raw):
    """ return the first category's name
    """

    def format(self, category):
        if len(category) == 0:
            return None
        else:
            return category[0].name


class TagItem(fields.Raw):
    """
    Return :
        return all the tags
    """

    def format(self, article_tag):
        tags = list()
        for tag in article_tag:
            tags.append(tag.name)
        return tags


class PostTimeItem(fields.Raw):
    """
    return the timestamp
    """

    def format(self, post_time):
        return post_time.timestamp()
        # t=datetime.fromtimestamp(postTime)
        # a = post_time.strftime('%Y-%m-%d %H:%M:%S')
        # return time.mktime(time.strptime(a, '%Y-%m-%d %H:%M:%S'))


class ImgToDataurl(fields.Raw):
    """
    return the image url
    """

    def format(self, img_url):
        return "/"+img_url


# work with marshal_with() to change a class into json
# used in pagnation
# paging = {
#     "limit": fields.Integer,
#     "offset": fields.Integer,
#     "total": fields.Integer
# }


article_data = {
    "id": fields.Integer(attribute="article_id"),
    "category": CategoryItem,
    "tags": TagItem,
    "post_time": PostTimeItem(attribute="post_time"),
    "title": fields.String(attribute="title"),
    "outline": fields.String(attribute="outline"),
    "status": fields.Integer(attribute="status"),
    "author": fields.String,
    "img_url": fields.String,

}
# Multiple articles' return fields
# article_fields = {
#     "paging": fields.Nested(paging),
#     "data": fields.Nested(article_data)
# }
# single article's return field
article_spec_fields = {
    "id": fields.Integer(attribute="article_id"),
    "category": CategoryItem,
    "tags": TagItem,
    "post_time": PostTimeItem(attribute="post_time"),
    "title": fields.String(attribute="title"),
    "outline": fields.String(attribute="outline"),
    "status": fields.Integer(attribute="status"),
    "author": fields.String,
    "detail": fields.String
}

slideshow_data = {
    "id": fields.Integer(attribute="slide_id"),
    "post_time": PostTimeItem(attribute="post_time"),
    "img_url": ImgToDataurl(attribute="img_url"),
    "outline": fields.String,
    "status": fields.Integer,
    "link": fields.String,
    "title": fields.String
}
# multiple slideshows' return fields
# slideshow_fields = {
#     "paging": fields.Nested(paging),
#     "data": fields.Nested(slideshow_data)
# }


class SlideshowsApi(Resource):
    """ 
    Resource for '/api/news/slide-shows'
    """

    @marshal_with(slideshow_data)
    def get(self):

        slide_shows = SlideShow.query.all()
        return slide_shows

    def post(self):

        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "POST":
            permission = Permission(ActionNeed('添加文章'))
            if permission.can() is not True:
                abort_if_unauthorized("添加文章")
            slideshow_args = slideshow_parser.parse_args()
            title = slideshow_args['title']
            img_url = slideshow_args['img_url']
            try:
                img_url = dataurl_to_img(img_url)
                print(img_url)
            except:
                pass
            outline = slideshow_args['outline']
            link = slideshow_args['link']
            slide_show = SlideShow(title, img_url, outline, link)
            aun_db.session.add(slide_show)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class SlideshowApi(Resource):
    """ 
    Resource for '/api/news/slide-shows/id'
    """

    @marshal_with(slideshow_data)
    def get(self, slideshow_id):

        slide_show = SlideShow.query.filter(
            SlideShow.slide_id == slideshow_id).first()
        abort_if_not_exist(slide_show, "slide_show")
        return slide_show

    def post(self, slideshow_id):

        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "PUT":
            permission = Permission(ActionNeed('修改文章'))
            if permission.can()is not True:
                abort_if_unauthorized("修改文章")
            slide_show = SlideShow.query.filter(
                SlideShow.slide_id == slideshow_id).first()
            abort_if_not_exist(slide_show, "slide_show")
            args = slideshow_spec_parser.parse_args()
            title = args['title']
            img_url = args['img_url']
            try:
                img_url = dataurl_to_img(img_url)
            except:
                img_url = args['img_url']
            outline = args['outline']
            status = args['status']
            link = args['link']
            if title != None:
                slide_show.title = title
            if img_url != None:
                slide_show.img_url = img_url
            if outline != None:
                slide_show.outline = outline
            if status != None:
                slide_show.status = status
            if link != None:
                slide_show.link = link
            aun_db.session.add(slide_show)
            aun_db.session.commit()
        elif request_method == "DELETE":
            permission = Permission(ActionNeed('删除文章'))
            if permission.can()is not True:
                abort_if_unauthorized("删除文章")
            slide_show = SlideShow.query.filter(
                SlideShow.slide_id == slideshow_id).first()
            abort_if_not_exist(slide_show, "slide_show")
            aun_db.session.delete(slide_show)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class ArticlesApi(Resource):
    """ 
    Resource for /api/news/news,
             /api/clubs/<string:club_id>/articles)
    """

    @marshal_with(article_data)
    def get(self, club_id=0):
        """
            Return:
                if club_id !=0 then return this club's atrical
        """
        if club_id != 0:
            club = Club.query.filter(
                Club.club_id == club_id).first()
            abort_if_not_exist(club, "club")
            article = club.articles
        else:
            article_temp = Article.query.filter().all()
            article = []  # only show article that doesn't belong to club
            for n in article_temp:
                clubs = []
                for c in n.club:
                    clubs.append(c.name)
                if len(clubs) == 0:
                    article.append(n)

        return article

    def post(self, club_id=0):
        """
        """
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']

        if request_method == "POST":
            if club_id != 0:
                club = Club.query.filter(
                    Club.club_id == club_id).first()
                abort_if_not_exist(club, "club")

                permission = Permission(ActionNeed('添加文章'))
                if permission.can()is not True and club not in current_user.clubs:
                    abort_if_unauthorized("添加文章")
            else:
                permission = Permission(ActionNeed('添加文章'))
                if permission.can() != True:
                    abort_if_unauthorized("添加文章")

            article_args = article_parser.parse_args()
            detail = article_args['detail']
            title = article_args['title']
            tags = article_args['tags']
            try:
                tags = list(eval(tags[0]))
            except:
                pass
            # tags = json.loads(tags)
            soup, img_url_first = handle_html(detail)
            outline = soup.get_text()[:80]

            article = Article(soup.prettify(), title, outline, img_url_first)
            aun_db.session.add(article)
            aun_db.session.commit()

            article.add_category(category)
            for tag in tags:
                t = Tag.query.filter_by(name=tag).first()
                abort_if_not_exist(t, "tag")
                article.tags.append(t)

            aun_db.session.add(article)
            aun_db.session.commit()
            if club_id != 0:
                club.add_article(article)
                aun_db.session.add(club)
                aun_db.session.commit()

        else:
            abort(404, message="api not found")


class ArticleApi(Resource):
    """ 
    Resoruce for 
            "/api/news/news/<string:id>",
            "/api/clubs/<string:club_id>/articles/<string:article_id>")
    """

    @marshal_with(article_spec_fields)
    def get(self, article_id, club_id=0):
        """
        Return :
            if club_id !=0 then return this club' some article
        """
        if club_id != 0:
            club = Club.query.filter(
                Club.club_id == club_id).first()
            abort_if_not_exist(club, "club")
            articles = club.articles
            article = Article.query.filter(
                Article.article_id == article_id).first()
            if article in articles:
                return article
            else:
                abort_if_not_exist(article, "this article")
        else:
            article = Article.query.filter(
                Article.article_id == article_id).first()
            return article

    def post(self, article_id, club_id=0):
        """
        if club_id != 0 then handle some club' s some article
        """
        article = Article.query.filter(
            Article.article_id == article_id).first()
        abort_if_not_exist(article, "article")

        if club_id != 0:
            club = Club.query.filter(
                Club.club_id == club_id).first()
            abort_if_not_exist(club, "club")

            articles = club.articles
            if article not in articles:  # this club doesn't have this article
                abort_if_not_exist(article, "this article")

        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "PUT":

            permission = Permission(ActionNeed('修改文章'))
            if permission.can()is not True:
                abort_if_unauthorized("修改文章")

            args = article_spec_parser.parse_args()
            category = args['category']
            detail = args['detail']
            title = args['title']
            status = args['status']
            tags = args['tags']
            try:
                tags = list(eval(tags[0]))
            except:
                pass
            # tags = json.dumps(tags)
            if category != None:
                article.category = []
                article.add_category(category)
            if detail != None:
                article.detail = detail
                soup, img_url_first = handle_html(detail)
                article.img_url = img_url_first
                outline = soup.get_text()[:80]
                article.outline = outline

            if title != None:
                article.title = title

            if status != None:
                article.status = status
            if tags != None:
                article.tags = []
                for tag in tags:
                    article.add_tag(tag)

            aun_db.session.add(article)
            aun_db.session.commit()

        elif request_method == "DELETE":
            permission = Permission(ActionNeed('删除文章'))
            if permission.can()is not True:
                abort_if_unauthorized("删除文章")

            aun_db.session.delete(article)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class ArticleDetailApi(Resource):
    """ 
    Resoruce for /api/news/news/<string:id>/detail",

    """

    def get(self, article_id):

        # id=int(id)
        article = Article.query.filter(
            Article.article_id == article_id).first()
        abort_if_not_exist(article, "article")
        data = dict()
        data['detail'] = article.detail
        return data


class CategorysApi(Resource):
    """
    Resource for /api/article/categorys
    """

    def get(self):

        categorys = Category.query.all()
        datas = list()
        for category in categorys:
            data = dict()
            data['name'] = category.name
            data['id'] = category.cat_id
            datas.append(data)
        return datas

    def post(self):

        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "POST":
            permission = Permission(ActionNeed("添加文章栏目"))
            if permission.can()is not True:
                abort_if_unauthorized("添加文章栏目")
            args = parser.parse_args()
            name = args['name']
            c = Category.query.filter(Category.name == name).first()
            abort_if_exist(c, "category")
            category = Category(name)
            aun_db.session.add(category)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class CategoryApi(Resource):
    """ 
    Resoruce for '/api/article/categorys/id'
    """

    def get(self, cat_id):
        """ method docstring
        """
        category = Category.query.filter_by(cat_id=cat_id).first()
        abort_if_not_exist(category, "category")
        data = dict()
        data['name'] = category.name
        data['id'] = category.cat_id
        return data

    def post(self, cat_id):

        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "PUT":
            permission = Permission(ActionNeed('修改文章栏目'))
            if permission.can()is not True:
                abort_if_unauthorized("修改文章栏目")

            category = Category.query.filter(Category.cat_id == cat_id).first()
            abort_if_not_exist(category, "category")
            args = parser_spec.parse_args()
            name = args['name']
            if name != None and name != category.name:
                c = Category.query.filter(Category.name == name).first()
                abort_if_exist(c, "category")
                category.name = name
            aun_db.session.add(category)
            aun_db.session.commit()

        elif request_method == "DELETE":
            permission = Permission(ActionNeed('删除文章栏目'))
            if permission.can()is not True:
                abort_if_unauthorized("删除文章栏目")
            cat_id = int(cat_id)
            category = Category.query.filter(Category.cat_id == cat_id).first()
            abort_if_not_exist(category, "category")
            aun_db.session.delete(category)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class TagsApi(Resource):
    """ 
    rest resoruce for /api/article/tags
    """

    def get(self):

        tags = Tag.query.all()
        datas = list()
        for tag in tags:
            data = dict()
            data['name'] = tag.name
            data['id'] = tag.tag_id
            datas.append(data)
        return datas

    def post(self):

        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "POST":
            permission = Permission(ActionNeed('添加文章标签'))
            if permission.can()is not True:
                abort_if_unauthorized("添加文章标签")
            args = parser.parse_args()
            name = args['name']
            t = Tag.query.filter(Tag.name == name).first()
            abort_if_exist(t, "tag")
            tag = Tag(name)
            aun_db.session.add(tag)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class TagApi(Resource):
    """
    rest resoruce for /api/article/tags/id

    """

    def get(self, id):

        tag = Tag.query.filter_by(tag_id=id).first()
        abort_if_not_exist(tag, "tag")
        data = dict()
        data['name'] = tag.name
        data['id'] = tag.tag_id
        return data

    def post(self, id):
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "PUT":
            permission = Permission(ActionNeed('修改文章标签'))
            if permission.can()is not True:
                abort_if_unauthorized("修改文章标签")
            tag = Tag.query.filter(Tag.tag_id == id).first()
            abort_if_not_exist(tag, "tag")
            args = parser_spec.parse_args()
            name = args['name']
            if name != None and name != tag.name:
                t = Tag.query.filter(Tag.name == name).first()
                abort_if_exist(t, "tag")
                tag.name = name
            aun_db.session.add(tag)
            aun_db.session.commit()
        elif request_method == "DELETE":
            permission = Permission(ActionNeed('删除文章标签'))
            if permission.can()is not True:
                abort_if_unauthorized("删除文章标签")
            tag = Tag.query.filter(Tag.tag_id == id).first()
            abort_if_not_exist(tag, "tag")
            aun_db.session.delete(tag)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")
