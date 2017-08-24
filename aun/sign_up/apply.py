"""
apply to join AU related
"""

from flask_restful import reqparse, abort, Resource, fields, marshal_with
from flask_principal import Permission, ActionNeed

from aun.sign_up.models import Applicant
from aun.common import request_method_parser, abort_if_not_exist, abort_if_unauthorized
from aun import aun_db

applicant_parser = reqparse.RequestParser()
applicant_parser.add_argument("name", type=str)
applicant_parser.add_argument("gender", type=str)
applicant_parser.add_argument("major", type=str)
applicant_parser.add_argument("phone", type=str)
applicant_parser.add_argument("first_choice", type=str)
applicant_parser.add_argument("second_choice", type=str)
applicant_parser.add_argument("is_adjust", type=bool)
applicant_parser.add_argument("self_introductionf", type=str)


class ApplyTimeItem(fields.Raw):
    """
    return the timestamp
    """

    def format(self, post_time):
        return post_time.timestamp()


applicant_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "gender": fields.String,
    "major": fields.String,
    "phone": fields.String,
    "first_choice": fields.String,
    "second_choice": fields.String,
    "is_adjust": fields.Boolean,
    "self_introduction": fields.String,
    "apply_time": ApplyTimeItem(attribute="apply_time")
}


class ApplicantsApi(Resource):

    @marshal_with(applicant_fields)
    def get(self):
        applicants = Applicant.query.all()
        return applicants

    def post(self):
        request_arg = request_method_parser.parse_args()
        request_method = request_arg["request_method"]

        if request_method == "POST":
            applicant_args = applicant_parser.parse_args()
            name = applicant_args["name"]
            gender = applicant_args["gender"]
            major = applicant_args["major"]
            phone = applicant_args["phone"]
            first_choice = applicant_args["first_choice"]
            second_choice = applicant_args["second_choice"]
            is_adjust = applicant_args["is_adjust"]
            self_introduction = applicant_args["self_introduction"]

            applicant = Applicant(name, gender, major, phone, first_choice, second_choice,
                                  is_adjust, self_introduction)

            aun_db.session.add(applicant)
            aun_db.session.commit()


class ApplicantApi(Resource):

    @marshal_with(applicant_fields)
    def get(self, id):

        applicant = Applicant.query.fliter(Applicant.id == id).first()
        return applicant

    def post(self, id):
        request_arg = request_method_parser.parse_args()
        request_method = request_arg["request_method"]

        if request_method == "DELETE":
            permission = Permission(ActionNeed("删除报名人员"))
            if permission.can() != True:
                abort_if_unauthorized("删除报名人员")

            applicant = Applicant.query.fliter(Applicant.id == id).first()
            abort_if_not_exist(applicant, "this applicant")

            aun_db.session.delete(applicant)
            aun_db.session.commit()


class ApplicantsDownloadApi(Resource):

    def get(self):
        pass
