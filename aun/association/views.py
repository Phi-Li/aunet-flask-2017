# -*-coding:utf-8 -*-
"""
register the rest api
"""

from aun.association.association import ClubApi, ClubsApi, ClubIntorduction
from aun import aun_api

aun_api.add_resource(ClubApi, "/api/clubs/<string:club_id>", endpoint="club")
aun_api.add_resource(ClubsApi, "/api/clubs", endpoint="clubs")
aun_api.add_resource(
    ClubIntorduction, "/api/clubs/<string:club_id>/introduction")
