# -*-coding:utf-8 -*-
""" module docstring
"""
from datetime import datetime
from flask_restful import reqparse, Resource,  marshal_with

from aun.home.models import Article
from aun.admin.news import article_fields


article_parser = reqparse.RequestParser()
article_parser.add_argument(
    "category", type=str, required=True, help="category is needed")
article_parser.add_argument(
    'sort', type=str, required=True, help="sort is needed")
article_parser.add_argument(
    'start', type=int, required=True, help="start is needed")
article_parser.add_argument(
    'end', type=int, required=True, help="end is needed")
article_parser.add_argument(
    'tags', type=str, required=True, action="append", help="tags is needed")


class SearchArticleApi(Resource):
    """ 
    rest resource for /api/search/article
    """

    @marshal_with(article_fields)
    def get(self):

        data = list()
        args = article_parser.parse_args()
        category = args['category']
        sort = args['sort']
        start = args['start']
        end = args['end']
        tags = args['tags']
        try:
            tags = list(eval(tags[0]))
        except:
            pass
        start = float(start)
        end = float(end)
        start = datetime.fromtimestamp(start)
        end = datetime.fromtimestamp(end)
        article = Article.query.filter(
            Article.post_time < end, Article.post_time >= start).all()
        for new in article:
            new_tags = list()
            for tag in new.tags:
                new_tags.append(tag.name)
            cate = new.category[0].name
            if set(tags).issubset(set(new_tags)) is True and cate == category:
                data.append(new)
        return data
