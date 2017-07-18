# -*-coding:utf-8 -*-

""" manage news
"""
import time
import random
from io import BytesIO
from urllib import request
import os
import base64
from bs4 import BeautifulSoup
from PIL import Image

from flask_restful import reqparse, abort, Resource, fields, marshal_with
from flask_principal import Permission, ActionNeed

# import models needed
from aun import aun_db, aun_app
from aun.home.models import News, SlideShow, Category, Tag

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
    "editable", type=int, location='json', help="status")
slideshow_spec_parser.add_argument(
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


news_spec_parser = reqparse.RequestParser()
news_spec_parser.add_argument(
    "category", type=str, location="json", help="category")
news_spec_parser.add_argument(
    "detail", type=str, location="json", help="detail")
news_spec_parser.add_argument("title", type=str, location="json", help="title")
news_spec_parser.add_argument(
    "editable", type=int, location="json", help="edit status")
news_spec_parser.add_argument(
    "tags", type=str, location="json", action='append', help="tags id is needed")
news_spec_parser.add_argument('detail', type=str, location="json")


# Request parser for slideshow
parser = reqparse.RequestParser()
parser.add_argument(
    'name', type=str, location='json', help="name is needed", required=True)

parser_spec = reqparse.RequestParser()
parser_spec.add_argument('name', type=str, location='json')

# parser to judge DELETE or POST or PUT http method
request_method_parser = reqparse.RequestParser()
request_method_parser.add_argument('request_method', type=str, location='json')


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

    def format(self, post_time):
        # t=datetime.fromtimestamp(postTime)
        a = post_time.strftime('%Y-%m-%d %H:%M:%S')
        return time.mktime(time.strptime(a, '%Y-%m-%d %H:%M:%S'))


class ImgToDataurl(fields.Raw):
    """ class docstring
    """

    def format(self, img_url):
        return "/"+img_url


# work with marshal_with() to change a class into json
news_fields = {
    "id": fields.Integer(attribute="news_id"),
    "category": CategoryItem,
    "tags": TagItem,
    "post_time": PostTimeItem(attribute="post_time"),
    "title": fields.String(attribute="title"),
    "outline": fields.String(attribute="outline"),
    "editable": fields.Integer(attribute="editable"),
    "author": fields.String
}
news_spec_parser = {
    "id": fields.Integer(attribute="news_id"),
    "category": CategoryItem,
    "tags": TagItem,
    "post_time": PostTimeItem(attribute="post_time"),
    "title": fields.String(attribute="title"),
    "outline": fields.String(attribute="outline"),
    "editable": fields.Integer(attribute="editable"),
    "author": fields.String,
    "detail": fields.String
}
slideshow_fields = {
    "id": fields.Integer,
    "post_time": PostTimeItem(attribute="post_time"),
    "img_url": ImgToDataurl(attribute="img_url"),
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
        i.save(path, quality="192")
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
        slide_shows = SlideShow.query.all()
        return slide_shows

    def post(self):
        """ method docstring
        """
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "POST":
            permission = Permission(ActionNeed('添加新闻'))
            if permission.can() is not True:
                abort_if_unauthorized("添加新闻")
            slideshow_args = slideshow_parser.parse_args()
            title = slideshow_args['title']
            img_url = slideshow_args['img_url']
            try:
                img_url = dataurl_to_img(img_url)
            except:
                pass
            outline = slideshow_args['outline']
            link = slideshow_args['link']
            slide_show = SlideShow(title, img_url, outline, link)
            aun_db.session.add(slide_show)
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
        slide_show = SlideShow.query.filter(
            SlideShow.slide_id == slideshow_id).first()
        abort_if_not_exist(slide_show, "slide_show")
        return slide_show

    def post(self, slideshow_id):
        """ method docstring
        """
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "PUT":
            permission = Permission(ActionNeed('修改新闻'))
            if permission.can()is not True:
                abort_if_unauthorized("修改新闻")
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
            editable = args['editable']
            link = args['link']
            if title != None:
                slide_show.title = title
            if img_url != None:
                slide_show.img_url = img_url
            if outline != None:
                slide_show.outline = outline
            if editable != None:
                slide_show.editable = editable
            if link != None:
                slide_show.link = link
            aun_db.session.add(slide_show)
            aun_db.session.commit()
        elif request_method == "DELETE":
            permission = Permission(ActionNeed('删除新闻'))
            if permission.can()is not True:
                abort_if_unauthorized("删除新闻")
            slide_show = SlideShow.query.filter(
                SlideShow.slide_id == slideshow_id).first()
            abort_if_not_exist(slide_show, "slide_show")
            aun_db.session.delete(slide_show)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class NewsClass(Resource):
    """ class docstring
    """

    @marshal_with(news_fields)
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
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
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

    @marshal_with(news_spec_parser)
    def get(self, news_id):
        """ method docstring
        """
        permission = Permission(ActionNeed(('查看新闻')))
        if permission.can() is not True:
            abort_if_unauthorized("查看新闻")
        news = News.query.filter(News.news_id == news_id).first()
        abort_if_not_exist(news, "news")
        return news

    def post(self, news_id):
        """ method docstring
        """
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "PUT":
            permission = Permission(ActionNeed('修改新闻'))
            if permission.can()is not True:
                abort_if_unauthorized("修改新闻")
            news = News.query.filter(News.news_id == news_id).first()
            abort_if_not_exist(news, "news")
            args = news_spec_parser.parse_args()
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

            news = News.query.filter(News.news_id == news_id).first()
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
        news = News.query.filter(News.news_id == news_id).first()
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
            data['id'] = category.cat_id
            datas.append(data)
        return datas

    def post(self):
        """ method docstring
        """
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
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
        data['id'] = category.cat_id
        return data

    def post(self, cat_id):
        """ method docstring
        """
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "PUT":
            permission = Permission(ActionNeed('修改新闻属性'))
            if permission.can()is not True:
                abort_if_unauthorized("修改新闻属性")

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
            permission = Permission(ActionNeed('删除新闻属性'))
            if permission.can()is not True:
                abort_if_unauthorized("删除新闻属性")
            cat_id = int(cat_id)
            category = Category.query.filter(Category.cat_id == cat_id).first()
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
            data['id'] = tag.tag_id
            datas.append(data)
        return datas

    def post(self):
        """ method docstring
        """
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
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
            permission = Permission(ActionNeed('修改新闻标签'))
            if permission.can()is not True:
                abort_if_unauthorized("修改新闻标签")
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
            permission = Permission(ActionNeed('删除新闻标签'))
            if permission.can()is not True:
                abort_if_unauthorized("删除新闻标签")
            tag = Tag.query.filter(Tag.tag_id == id).first()
            abort_if_not_exist(tag, "tag")
            aun_db.session.delete(tag)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")
