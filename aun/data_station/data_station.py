# -*-coding:utf-8 -*-

"""
 rest api for data station related
"""

from flask_restful import reqparse, Resource, fields, marshal_with, abort
from flask_principal import Permission, ActionNeed
from flask_login import current_user
from flask import current_app

import os
import werkzeug

from aun.data_station.models import DataStation
from aun.common import request_method_parser, abort_if_not_exist, abort_if_unauthorized
from aun import aun_db

file_parser = reqparse.RequestParser()
file_parser.add_argument(
    "file", type=werkzeug.datastructures.FileStorage, required=True, location="files")

file_filter_parser = reqparse.RequestParser()
file_filter_parser.add_argument("status", type=int, required=True)
file_filter_parser.add_argument("is_important", type=int, required=True)

# data staion parser for put method
file_put_parser = reqparse.RequestParser()
file_put_parser.add_argument("file_name", type=str)
file_put_parser.add_argument(
    "file", type=werkzeug.datastructures.FileStorage, location="files")
file_put_parser.add_argument("status", type=int)
file_put_parser.add_argument("is_important", type=int)


class ToTimestamp(fields.Raw):
    """ 
    return the timestamp 
    """

    def format(self, upload_time):
        return upload_time.timestamp()

file_field = {
    "id": fields.Integer(attribute="file_id"),
    "file_name": fields.String,
    "uploader": fields.String,
    "download_times": fields.Integer,
    "upload_time":  ToTimestamp(attribute="upload_time")}


class DataStationsApi(Resource):

    @marshal_with(file_field)
    def get(self):
        file_filter = file_filter_parser.parse_args()
        status = file_filter_parser["status"]
        is_important = file_filter_parser["is_important"]

        files = DataStation.query.filter(
            DataStation.status == status, DataStation.is_important == is_important).all()

        return files

    def post(self):
        request_arg = request_method_parser.parse_args()
        request_method = request_arg["request_method"]

        if request_method == "POST":
            permission = Permission(ActionNeed("上传文件"))
            if permission.can() != True:
                abort_if_unauthorized("上传文件")

            file_arg = file_parser.parse_args()
            file = file_arg["file"]

            file_name = file.file_name
            uploader = current_user.user_nam
            file_dir = os.path.join(
                current_app.config["BASEDIR"], "aun/static/upload/data_station")

            file_path = os.path.join(file_dir, file_name)
            file.save(file_path)
            file.close()

            data = DataStation(file_name, uploader)

            aun_db.session.add(data)
            aun_db.session.commit()


class DataStationApi(Resource):

    @marshal_with(file_field)
    def get(self, file_id):
        file = DataStation.query.filter(DataStation.file_id == file_id).first()
        abort_if_not_exist(file, "this file")

        return file

    def post(self, file_id):
        file = DataStation.query.filter(DataStation.file_id == file_id).first()
        abort_if_not_exist(file, "this file")

        request_arg = request_method_parser.parse_args()
        request_method = request_arg["request_method"]

        if request_method == "PUT":
            permission = Permission(ActionNeed("修改文件属性"))  # 包括审核文件，　设置红头文件
            if permission.can() != True:
                abort_if_unauthorized("修改文件属性")
            args = file_put_parser.parse_args()
            file_content = args['file']
            file_name = file["file_name"]
            status = file["status"]
            is_important = file["is_important"]

            if file_name != None:
                file.file_name = file_name
            if status != None:
                file.status = status
            if is_important != None:
                file.is_important = is_important
            if file_content != None:
                file.file_name = file_content.file_name
                file_dir = os.path.join(
                    current_app.config["BASEDIR"], "aun/static/upload/data_station")

                file_path = os.path.join(file_dir, file_name)
                file.save(file_path)
                file.close()

            aun_db.session.add(file)
            aun_db.session.commit()

        elif request_method == "DELETE":
            permission = Permission(ActionNeed("删除文件"))

            if permission.can() != True:
                abort_if_unauthorized("删除文件")
            aun_db.session.delete(file)
            aun_db.session.commit()


class DataDownloadApi(Resource):

    def get(self, file_id):
        file = DataStation.query.filter(DataStation.file_id == file_id).first()
        abort_if_not_exist(file, "this file")

        file.download_times = file.download_times+1

        file_dir = os.path.join(
            current_app.config["BASEDIR"], "aun/static/upload/data_station")

        return send_from_directory(file_dir, file.file_name, as_attachment=True)
