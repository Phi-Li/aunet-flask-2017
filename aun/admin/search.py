# -*-coding:utf-8 -*-
""" module docstring
"""
from datetime import datetime
from flask_restful import reqparse, Resource,  marshal_with

from aun.home.models import Article
from aun.admin.news import article_data


article_parser = reqparse.RequestParser()
article_parser.add_argument(
    "keyword", type=str, required=True, help="search keyword")
article_parser.add_argument(
    "club_id", type=int)


class SearchArticleApi(Resource):
    """ 
    rest resource for /api/search/article
    """

    @marshal_with(article_data)
    def get(self, club_id=0):
        search_arg = article_parser.parse_args()

        keyword = search_arg["keyword"]

        if club_id != 0:
            articles_temp = Article.query.msearch(
                keyword, fields=["title", "detail"]).filter(Article.club != None).all()
            articles = list()
            for article in articles_temp:
                if article.club[0].club_id == club_id:
                    articles.append(article)

        else:
            articles = Article.query.msearch(
                keyword, fields=["title", "detail"]).filter(Article.club == None).all()

        return articles
