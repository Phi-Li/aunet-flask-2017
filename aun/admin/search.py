# -*-coding:utf-8 -*-
""" module docstring
"""
from datetime import datetime
from flask_restful import reqparse, abort, Resource, fields, marshal_with

from aun.home.models import News
from aun import aun_db
from .news import News_fields


News_parser = reqparse.RequestParser()
News_parser.add_argument(
    "category", type=str, required=True, help="category is needed")
News_parser.add_argument(
    'sort', type=str, required=True, help="sort is needed")
News_parser.add_argument(
    'start', type=int, required=True, help="start is needed")
News_parser.add_argument('end', type=int, required=True, help="end is needed")
News_parser.add_argument(
    'tags', type=str, required=True, action="append", help="tags is needed")


class SearchNews(Resource):
    """ class docstring
    """

    @marshal_with(News_fields)
    def get(self):
        """ method docstring
        """
        data = list()
        # data1=dict()
        args = News_parser.parse_args()
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
        news = News.query.filter(
            News.post_time < end, News.post_time >= start).all()
        for new in news:
            new_tags = list()
            for tag in new.tags:
                new_tags.append(tag.name)
            cate = new.category[0].name
            if set(tags).issubset(set(new_tags)) is True and cate == category:
                data.append(new)
        return data
