# -*-coding:utf-8 -*-

"""
 rest api for club space related
"""
from flask_restful import reqparse, Resource, fields, marshal_with, abort
from flask_principal import Permission, ActionNeed
from flask_login import current_user

from aun.common import abort_if_unauthorized, dataurl_to_img, abort_if_exist
from aun.association.models import Club

request_method_parser = reqparse.RequestParser()
request_method_parser.add_argument('request_method', type=str, location='json')

club_parser = reqparse.RequestParser()
club_parser.add_argument(
    "name", type=str, location="json", help="club name")
club_parser.add_argument(
    "introduction", type=str, location="json", help="brief introduction")
club_parser.add_argument(
    "category", type=str, location="json", help="club category")
club_parser.add_argument(
    "picture", type=str, location="json", help="club picture ")

club_fields = {
    "id": fields.Integer(attribute="club_id"),
    "name": fields.String,
    "introduction": fields.String,
    "category": fields.String,
    "picture": fields.String
}


class ClubsApi(Resource):
    """
    rest api for club space related, request method: get, post
    """
    @marshal_with(club_fields)
    def get(self):
        clubs = Club.query.all()
        return clubs

    def post(self):
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "POST":
            permission = Permission(ActionNeed("添加社团"))
            if permission.can() is not True:
                abort_if_unauthorized("添加社团")
            club_args = club_parser.parse_args()
            name = club_args["name"]
            introduction = club_args["introduction"]
            category = club_args["category"]
            picture = club_args["picture"]
            try:
                # if picture is dataurl, then change it to url
                picture = dataurl_to_img(picture)
            except:
                pass
            club = Club(name, introduction, category, picture)
            aun_db.session.add(club)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class ClubApi(Resource):
    """
    request method: get, put, delete
    """
    @marshal_with(club_fields)
    def get(self, club_id):
        """
        Return:
            some club info 
        """
        club = Club.query.filter(
            Club.club_id == club_id).first()
        abort_if_not_exist(club, "club")
        return club

    def post(self, club_id):
        """
        request method: put , delete
        """
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "PUT":
            club = Club.query.filter(
                Club.club_id == club_id).first()
            abort_if_not_exist(club, "club")

            permission = Permission(ActionNeed("编辑社团空间"))
            if permission.can() != True or current_user.clubs[0] != club:
                abort_if_unauthorized("编辑社团空间")

            club_args = club_parser.parse_args()
            name = club_args["name"]
            introduction = club_args["introduction"]
            category = club_args["category"]
            picture = club_args["picture"]

            if name != None:
                club.name = name
            if introduction != None:
                club.introduction = introduction
            if category != None:
                club.category = category
            if picture != None:
                try:
                    # if picture is dataurl, then change it to url
                    picture = dataurl_to_img(picture)
                except:
                    pass
                club.picture = picture

            aun_db.session.add(club)
            aun_db.session.commit()
        elif request_method == "DELETE":
            club = Club.query.filter(
                Club.club_id == club_id).first()
            abort_if_not_exist(club, "club")

            permission = Permission(ActionNeed("删除社团"))
            if permission.can()is not True or current.clubs[0] != club:
                abort_if_unauthorized("删除社团")

            aun_db.session.delete(club)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")
