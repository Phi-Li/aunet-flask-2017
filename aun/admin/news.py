# -*-coding:utf-8 -*-

""" manage news
"""

from flask_restful import reqparse, abort, Resource, fields, marshal_with
from flask_principal import Permission, ActionNeed

from datetime import datetime
import time
from bs4 import BeautifulSoup
from io import BytesIO
from urllib import request
import random
import os
import base64
import json
from PIL import Image

# import models needed
from aun import aun_db, aun_app
from aun.home.models import News, slideshow, Category, Tag

# Request parser for slideshow
sildeshow_parser = reqparse.RequestParser()
sildeshow_parser.add_argument(
    'title', type=str, required=True, location="json", help="title is needed")
sildeshow_parser.add_argument(
    'imgUrl', type=str, required=True, location="json", help="imgUrl is needed")
sildeshow_parser.add_argument(
    "outline", type=str, required=True, location="json", help="outline is needed")
sildeshow_parser.add_argument(
    "link", type=str, required=True, location="json", help="the link that jump")


slideshowSpec_parser = reqparse.RequestParser()
slideshowSpec_parser.add_argument(
    'title', type=str, location="json", help="title")
slideshowSpec_parser.add_argument(
    'imgUrl', type=str, location="json", help="imgUrl")
slideshowSpec_parser.add_argument(
    "outline", type=str, location="json", help="outline")
slideshowSpec_parser.add_argument(
    "editable", type=int, location='json', help="status")
slideshowSpec_parser.add_argument(
    "link", type=str, location="json", help="the link that jump")

# Request parser for news
news_parser = reqparse.RequestParser()
news_parser.add_argument(
    "category", type=str, location="json", required=True, help="category  is needed")
news_parser.add_argument(
    "detail", type=str, location="json", required=True, help="detail is needed")
news_parser.add_argument(
    "title", type=str, location="json", required=True, help="title is needed")
news_parser.add_argument("tags", type=str, location="json",
                         required=True, action='append', help="tags  is needed")


NewsSpec_parser = reqparse.RequestParser()
NewsSpec_parser.add_argument(
    "category", type=str, location="json", help="category")
NewsSpec_parser.add_argument(
    "detail", type=str, location="json", help="detail")
NewsSpec_parser.add_argument("title", type=str, location="json", help="title")
NewsSpec_parser.add_argument(
    "editable", type=int, location="json", help="edit status")
NewsSpec_parser.add_argument(
    "tags", type=str, location="json", action='append', help="tags id is needed")
NewsSpec_parser.add_argument('detail', type=str, location="json")


# Request parser for slideshow
parser = reqparse.RequestParser()
parser.add_argument(
    'name', type=str, location='json', help="name is needed", required=True)

parser_spec = reqparse.RequestParser()
parser_spec.add_argument('name', type=str, location='json')

# parser to judge DELETE or POST or PUT http method
RequestMethod_parser = reqparse.RequestParser()
RequestMethod_parser.add_argument('requestMethod', type=str, location='json')


# defined as a new field
class CategoryItem(fields.Raw):
    """ class docstring
    """

    def format(self, category):
        if len(category) == 0:
            return None
        else:
            return category[0].name


class TagItem(fields.Raw):
    """ class docstring
    """

    def format(self, news_tag):
        tags = list()
        for tag in news_tag:
            tags.append(tag.name)
        return tags


class PostTimeItem(fields.Raw):
    """ class docstring
    """

    def format(self, postTime):
        # t=datetime.fromtimestamp(postTime)
        a = postTime.strftime('%Y-%m-%d %H:%M:%S')
        return time.mktime(time.strptime(a, '%Y-%m-%d %H:%M:%S'))


class ImgToDataurl(fields.Raw):
    """ class docstring
    """

    def format(self, imgUrl):
        try:
            path = os.path.join(aun_app.config['BASEDIR'], 'aunet', imgUrl)
            with open(path, "rb") as f:
                data = f.read()
            data = base64.b64encode(data)  #
            data = str(data)
            data = data[2:-1]
            data = "data:image/jpg;base64,"+data
            return data
        except:
            return imgUrl


# work with marshal_with() to change a class into json
News_fields = {
    "id": fields.Integer(attribute="id"),
    "category": CategoryItem,
    "tags": TagItem,
    "postTime": PostTimeItem(attribute="post_time"),
    "title": fields.String(attribute="title"),
    "outline": fields.String(attribute="outline"),
    "editable": fields.Integer(attribute="editable"),
    "author": fields.String
}
NewsSpec_fields = {
    "id": fields.Integer(attribute="id"),
    "category": CategoryItem,
    "tags": TagItem,
    "postTime": PostTimeItem(attribute="post_time"),
    "title": fields.String(attribute="title"),
    "outline": fields.String(attribute="outline"),
    "editable": fields.Integer(attribute="editable"),
    "author": fields.String,
    "detail": fields.String
}
slideshow_fields = {
    "id": fields.Integer,
    "postTime": PostTimeItem(attribute="post_time"),
    "imgUrl": ImgToDataurl(attribute="img_url"),
    "outline": fields.String,
    "editable": fields.Integer,
    "link": fields.String,
    "title": fields.String
}


# manage error message
def abort_if_not_exist(data, message):
    """ function docstring
    """
    if data is None:
        abort(404, message="{} Not Found".format(message))


def abort_if_exist(data, message):
    """ function docstring
    """
    if data != None:
        abort(
            400, message="{} has existed ,please try another".format(message))


def abort_if_unauthorized(message):
    """ function docstring
    """
    abort(401, message="{} permission Unauthorized".format(message))


# change the img url into dataurl ,and return the first image
def handle_html(html):
    """ function docstring
    """
    soup = BeautifulSoup(html, "html.parser")
    image_num = 0  # judge if  these
    for img in soup.find_all('img'):
        imgurl = img.get('src')
        data = request.urlopen(imgurl).read()
        img_buf = BytesIO(data)  # change image in ram to batesIo
        i = Image.open(img_buf)
        filename = str(int(random.uniform(1, 1000)+time.time()))+".png"
        path = os.path.join(
            aun_app.config['BASEDIR'], 'aunet/static/Uploads/News', filename)
        i.save(path, quality="96")
        with open(path, "rb") as f:
            data = f.read()
        data = base64.b64encode(data)  #
        data = str(data)
        data = data[2:-1]
        data = "data:image/jpg;base64,"+data
        img['src'] = data
        # return img
        image_num = image_num+1
        if image_num > 1:
            # remove extra images, only save the first image
            os.remove(path)
        else:
            img_url_first = "static/Uploads/News/"+filename
    if image_num == 0:
        # the default image file
        img_url_first = "static/Uploads/News/default.jpg"
    return soup, img_url_first

# change imgurl into img and save it ,and save the path to the mysql


def dataurl_to_img(img_url):
    """ function docstring
    """

    data = request.urlopen(img_url).read()
    img_buf = BytesIO(data)
    img = Image.open(img_buf)
    filename = str(int(random.uniform(1, 1000)+time.time()))+".png"
    path = os.path.join(
        aun_app.config['BASEDIR'], 'aunet/static/Uploads/News', filename)
    img.save(path, quality="192")
    return 'static/Uploads/News/'+filename


class SlideshowClass(Resource):
    """ class docstring
    """

    @marshal_with(slideshow_fields)
    def get(self):
        """ method docstring
        """
        permission = Permission(ActionNeed(('查看新闻')))
        if permission.can() is not True:
            abort_if_unauthorized("查看新闻")
        silder_shows = slideshow.query.all()
        return silder_shows

    def post(self):
        """ method docstring
        """
        request_arg = RequestMethod_parser.parse_args()
        request_method = request_arg['requestMethod']
        if request_method == "POST":
            permission = Permission(ActionNeed('添加新闻'))
            if permission.can() is not True:
                abort_if_unauthorized("添加新闻")
            slideshow_args = sildeshow_parser.parse_args()
            print(slideshow_args)
            title = slideshow_args['title']
            img_url = slideshow_args['imgUrl']
            try:
                img_url = dataurl_to_img(img_url)
            except:
                pass
            outline = slideshow_args['outline']
            link = slideshow_args['link']
            silder_show = slideshow(title, img_url, outline, link)
            aun_db.session.add(silder_show)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class SlideshowSpec(Resource):
    """ class docstring
    """

    @marshal_with(slideshow_fields)
    def get(self, slideshow_id):
        """ method docstring
        """
        permission = Permission(ActionNeed(('查看新闻')))
        if permission.can() is not True:
            abort_if_unauthorized("查看新闻")
        silder_show = slideshow.query.filter(slideshow.id == slideshow_id).first()
        abort_if_not_exist(silder_show, "silder_show")
        return silder_show

    def post(self, slideshow_id):
        """ method docstring
        """
        request_arg = RequestMethod_parser.parse_args()
        request_method = request_arg['requestMethod']
        if request_method == "PUT":
            permission = Permission(ActionNeed('修改新闻'))
            if permission.can()is not True:
                abort_if_unauthorized("修改新闻")
            silder_show = slideshow.query.filter(slideshow.id == slideshow_id).first()
            abort_if_not_exist(silder_show, "silder_show")
            args = slideshowSpec_parser.parse_args()
            title = args['title']
            img_url = args['imgUrl']
            try:
                img_url = dataurl_to_img(img_url)
            except:
                img_url = args['imgUrl']
            outline = args['outline']
            editable = args['editable']
            link = args['link']
            if title != None:
                silder_show.title = title
            if img_url != None:
                silder_show.img_url = img_url
            if outline != None:
                silder_show.outline = outline
            if editable != None:
                silder_show.editable = editable
            if link != None:
                silder_show.link = link
            aun_db.session.add(silder_show)
            aun_db.session.commit()
        elif request_method == "DELETE":
            permission = Permission(ActionNeed('删除新闻'))
            if permission.can()is not True:
                abort_if_unauthorized("删除新闻")
            silder_show = slideshow.query.filter(slideshow.id == id).first()
            abort_if_not_exist(silder_show, "silder_show")
            aun_db.session.delete(silder_show)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class NewsClass(Resource):
    """ class docstring
    """

    @marshal_with(News_fields)
    def get(self):
        """ method docstring
        """
        permission = Permission(ActionNeed(('查看新闻')))
        if permission.can() is not True:
            abort_if_unauthorized("查看新闻")
        news = News.query.all()
        return news

    def post(self):
        """ method docstring
        """
        request_arg = RequestMethod_parser.parse_args()
        request_method = request_arg['requestMethod']
        if request_method == "POST":
            permission = Permission(ActionNeed('添加新闻'))
            if permission.can()is not True:
                abort_if_unauthorized("添加新闻")
            news_args = news_parser.parse_args()
            category = news_args['category']
            detail = news_args['detail']
            title = news_args['title']
            tags = news_args['tags']
            try:
                tags = list(eval(tags[0]))
            except:
                pass
            soup, img_url_first = handle_html(detail)
            outline = soup.get_text()[:80]
            news = News(soup.prettify(), title, outline, img_url_first)
            aun_db.session.add(news)
            aun_db.session.commit()
            news.addCategory(category)
            for tag in tags:
                t = Tag.query.filter_by(name=tag).first()
                abort_if_not_exist(t, "tag")
                news.tags.append(t)
            aun_db.session.add(news)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class NewsSpec(Resource):
    """ class docstring
    """

    @marshal_with(NewsSpec_fields)
    def get(self, news_id):
        """ method docstring
        """
        permission = Permission(ActionNeed(('查看新闻')))
        if permission.can() is not True:
            abort_if_unauthorized("查看新闻")
        news = News.query.filter(News.id == news_id).first()
        abort_if_not_exist(news, "news")
        return news

    def post(self, news_id):
        """ method docstring
        """
        request_arg = RequestMethod_parser.parse_args()
        request_method = request_arg['requestMethod']
        if request_method == "PUT":
            permission = Permission(ActionNeed('修改新闻'))
            if permission.can()is not True:
                abort_if_unauthorized("修改新闻")
            news = News.query.filter(News.id == id).first()
            abort_if_not_exist(news, "news")
            args = NewsSpec_parser.parse_args()
            category = args['category']
            detail = args['detail']
            title = args['title']
            editable = args['editable']
            tags = args['tags']
            try:
                tags = list(eval(tags[0]))
            except:
                pass
            if category != None:
                news.category = []
                news.addCategory(category)
            if detail != None:
                news.detail = detail
                soup, img_url_first = handle_html(detail)
                news.img_url = img_url_first
                outline = soup.get_text()[:80]
                news.outline = outline

            if title != None:
                news.title = title

            if editable != None:
                news.editable = editable
            if tags != None:
                news.tags = []
                for tag in tags:
                    news.addTag(tag)
            aun_db.session.add(news)
            aun_db.session.commit()
        elif request_method == "DELETE":
            permission = Permission(ActionNeed('删除新闻'))
            if permission.can()is not True:
                abort_if_unauthorized("删除新闻")

            news = News.query.filter(News.id == id).first()
            abort_if_not_exist(news, "news")
            aun_db.session.delete(news)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class NewsSpecDetail(Resource):
    """ class docstring
    """

    def get(self, news_id):
        """ method docstring
        """
        # id=int(id)
        news = News.query.filter(News.id == news_id).first()
        abort_if_not_exist(news, "news")
        data = dict()
        data['detail'] = news.detail
        return data


class Categorys(Resource):
    """ class docstring
    """

    def get(self):
        """ method docstring
        """
        permission = Permission(ActionNeed(('查看新闻栏目')))
        if permission.can() is not True:
            abort_if_unauthorized("查看新闻栏目")
        categorys = Category.query.all()
        datas = list()
        for category in categorys:
            data = dict()
            data['name'] = category.name
            data['id'] = category.id
            datas.append(data)
        return datas

    def post(self):
        """ method docstring
        """
        request_arg = RequestMethod_parser.parse_args()
        request_method = request_arg['requestMethod']
        if request_method == "POST":
            permission = Permission(ActionNeed("添加新闻属性"))
            if permission.can()is not True:
                abort_if_unauthorized("添加新闻属性")
            args = parser.parse_args()
            name = args['name']
            c = Category.query.filter(Category.name == name).first()
            abort_if_exist(c, "category")
            category = Category(name)
            aun_db.session.add(category)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class CategoryClass(Resource):
    """ class docstring
    """

    def get(self, cat_id):
        """ method docstring
        """
        permission = Permission(ActionNeed(('查看新闻栏目')))
        if permission.can() is not True:
            abort_if_unauthorized("查看新闻栏目")
        category = Category.query.filter_by(id=cat_id).first()
        abort_if_not_exist(category, "category")
        data = dict()
        data['name'] = category.name
        data['id'] = category.id
        return data

    def post(self, cat_id):
        """ method docstring
        """
        request_arg = RequestMethod_parser.parse_args()
        request_method = request_arg['requestMethod']
        if request_method == "PUT":
            permission = Permission(ActionNeed('修改新闻属性'))
            if permission.can()is not True:
                abort_if_unauthorized("修改新闻属性")

            category = Category.query.filter(Category.id == cat_id).first()
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
            permission = Permission(ActionNeed('删除新闻属性'))
            if permission.can()is not True:
                abort_if_unauthorized("删除新闻属性")
            cat_id = int(cat_id)
            category = Category.query.filter(Category.id == cat_id).first()
            abort_if_not_exist(category, "category")
            aun_db.session.delete(category)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class Tags(Resource):
    """ class docstring
    """

    def get(self):
        """ method docstring
        """
        permission = Permission(ActionNeed(('查看新闻标签')))
        if permission.can() is not True:
            abort_if_unauthorized("查看新闻标签")
        tags = Tag.query.all()
        datas = list()
        for tag in tags:
            data = dict()
            data['name'] = tag.name
            data['id'] = tag.id
            datas.append(data)
        return datas

    def post(self):
        """ method docstring
        """
        request_arg = RequestMethod_parser.parse_args()
        request_method = request_arg['requestMethod']
        if request_method == "POST":
            permission = Permission(ActionNeed('修改新闻标签'))
            if permission.can()is not True:
                abort_if_unauthorized("修改新闻标签")
            args = parser.parse_args()
            name = args['name']
            t = Tag.query.filter(Tag.name == name).first()
            abort_if_exist(t, "tag")
            tag = Tag(name)
            aun_db.session.add(tag)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class TagClass(Resource):

    def get(self, id):
        permission = Permission(ActionNeed(('查看新闻标签')))
        if permission.can() is not True:
            abort_if_unauthorized("查看新闻标签")
        tag = Tag.query.filter_by(id=id).first()
        abort_if_not_exist(tag, "tag")
        data = dict()
        data['name'] = tag.name
        data['id'] = tag.id
        return data

    def post(self, id):
        request_arg = RequestMethod_parser.parse_args()
        requestMethod = request_arg['requestMethod']
        if requestMethod == "PUT":
            permission = Permission(ActionNeed('修改新闻标签'))
            if permission.can()is not True:
                abort_if_unauthorized("修改新闻标签")
            tag = Tag.query.filter(Tag.id == id).first()
            abort_if_not_exist(tag, "tag")
            args = parser_spec.parse_args()
            name = args['name']
            if name != None and name != tag.name:
                t = Tag.query.filter(Tag.name == name).first()
                abort_if_exist(t, "tag")
                tag.name = name
            aun_db.session.add(tag)
            aun_db.session.commit()
        elif requestMethod == "DELETE":
            permission = Permission(ActionNeed('删除新闻标签'))
            if permission.can()is not True:
                abort_if_unauthorized("删除新闻标签")
            tag = Tag.query.filter(Tag.id == id).first()
            abort_if_not_exist(tag, "tag")
            aun_db.session.delete(tag)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")
