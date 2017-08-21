# -*-coding:utf-8 -*-
"""
register the rest api
"""

from aun.association.association import AssociationApi, AssociationsApi
from aun.admin.article import ArticlesApi, ArticleApi
from aun import aun_api

aun_api.add_resource(AssociationApi, "/api/associations/<string:id>")
aun_api.add_resource(AssociationsApi, "/api/associations")
aun_api.add_resource(
    ArticlesApi, "/api/associations/<string:association_id>/articles")
aun_api.add_resource(
    ArticleApi, "/api/associations/<string:association_id>/articles/<string:article_id>")
