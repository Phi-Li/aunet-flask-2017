# -*-coding:utf-8 -*-
"""
register the rest api
"""

from aun.club.club import ClubApi, ClubsApi
from aun.admin.article import ArticlesApi, ArticleApi
from aun import aun_api

aun_api.add_resource(ClubApi, "/api/clubs/<string:id>")
aun_api.add_resource(ClubsApi, "/api/clubs")
aun_api.add_resource(
    ArticlesApi, "/api/clubs/<string:club_id>/articles")
aun_api.add_resource(
    ArticleApi, "/api/clubs/<string:club_id>/articles/<string:article_id>")
