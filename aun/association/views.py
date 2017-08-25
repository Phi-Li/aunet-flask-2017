# -*-coding:utf-8 -*-
"""
register the rest api
"""

from aun.association.association import ClubApi, ClubsApi
from aun import aun_api

aun_api.add_resource(ClubApi, "/api/clubs/<string:id>", endpoint="club")
aun_api.add_resource(ClubsApi, "/api/clubs", endpoint="clubs")
