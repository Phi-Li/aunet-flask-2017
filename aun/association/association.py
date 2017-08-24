# -*-coding:utf-8 -*-

"""
 rest api for association space related
"""
from flask_restful import reqparse, Resource, fields, marshal_with, abort
from flask_principal import Permission, ActionNeed
from flask_login import current_user

from aun.admin.article import abort_if_unauthorized, dataurl_to_img, abort_if_exist

request_method_parser = reqparse.RequestParser()
request_method_parser.add_argument('request_method', type=str, location='json')

association_parser = reqparse.RequestParser()
association_parser.add_argument(
    "name", type=str, location="json", help="association name")
association_parser.add_argument(
    "introduction", type=str, location="json", help="brief introduction")
association_parser.add_argument(
    "category", type=str, location="json", help="association category")
association_parser.add_argument(
    "picture", type=str, location="json", help="association picture ")

association_fields = {
    "id": fields.Integer(attribute="association_id"),
    "name": fields.String,
    "introduction": fields.String,
    "category": fields.String,
    "picture", fields.String
}


class AssociationsApi(Resource)
"""
rest api for association space related, request method: get, post
"""
    @marshal_with(association_fields)
    def get(self):
        associations = Association.query, all()
        return associations

    def post(self):
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "POST":
            permission = Permission(ActionNeed("添加社团"))
            if permission.can() is not True:
                abort_if_unauthorized("添加社团")
            association_args = association_parser.parse_args()
            name = association_args["name"]
            introduction = association_args["introduction"]
            category = association_args["category"]
            picture = association_args["picture"]
            try:
                # if picture is dataurl, then change it to url
                picture = dataurl_to_img(picture)
            except:
                pass
            association = Association(name, introduction, category, picture)
            aun_db.session.add(association)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")


class AssociationApi(Resource)
    """
    request method: get, put, delete
    """
    @marshal_with(association_fields)
    def get(self, association_id):
        """
        Return:
            some association info 
        """
        association = Association.query.filter(
            Association.association_id == association_id).first()
        abort_if_not_exist(association, "association")
        return association

    def post(self, association_id):
    """
    request method: put , delete
    """
        request_arg = request_method_parser.parse_args()
        request_method = request_arg['request_method']
        if request_method == "PUT":
            association = Association.query.filter(
                Association.association_id == association_id).first()
            abort_if_not_exist(association, "association")

            permission = Permission(ActionNeed("编辑社团空间"))
            if permission.can() is not True　or current.associations[0] != association:
                abort_if_unauthorized("编辑社团空间")

            association_args = association_parser.parse_args()
            name = association_args["name"]
            introduction = association_args["introduction"]
            category = association_args["category"]
            picture = association_args["picture"]

            if name != None:
                association.name = name
            if introduction != None:
                association.introduction = introduction
            if category != None:
                association.category = category
            if picture != None:
                try:
                    # if picture is dataurl, then change it to url
                    picture = dataurl_to_img(picture)
                except:
                    pass
                association.picture = picture

            aun_db.session.add(association)
            aun_db.session.commit()
        elif request_method == "DELETE":
            association = Association.query.filter(
                Association.association_id == association_id).first()
            abort_if_not_exist(association, "association")

            permission = Permission(ActionNeed("删除社团"))
            if permission.can()is not True or current.associations[0] != association:
                abort_if_unauthorized("删除社团")

            aun_db.session.delete(association)
            aun_db.session.commit()
        else:
            abort(404, message="api not found")
